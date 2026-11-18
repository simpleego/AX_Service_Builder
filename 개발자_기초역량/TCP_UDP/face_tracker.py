"""
웹캠 실시간 얼굴 검출 + 추적 + 특징점 표시 (MediaPipe Face Landmarker)

- 얼굴 하나당 478개의 특징점(landmark)을 찾는다.
- 눈, 눈썹, 홍채(눈동자), 코, 입술, 얼굴 윤곽을 색깔별로 표시한다.
- 귀: MediaPipe 특징점에는 귀가 없으므로, 얼굴 윤곽 양 끝(귀 바로 앞)을 기준으로
       위치를 "추정"하고, 고개 방향으로 보이는 귀 / 가려진 귀를 구분한다.
- 안경: 두 눈 사이(콧등 위)에 안경 브리지의 강한 가로 경계선이 있는지로 판별한다.
- VIDEO 모드로 실행해서 이전 프레임의 결과를 이용해 얼굴을 추적한다.
- 코끝의 이동 경로를 꼬리처럼 그려서 추적되는 모습을 보여준다.

준비: pip install mediapipe opencv-python
실행: python face_tracker.py
키:   q 또는 ESC 종료 (창의 X 버튼, 터미널 Ctrl+C로도 종료)
      m 얼굴 메쉬(그물망) 켜기·끄기 / t 이동 경로 켜기·끄기
"""

import os
import time
import urllib.request
from collections import deque

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions, vision

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "face_landmarker.task")
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/"
             "face_landmarker/face_landmarker/float16/1/face_landmarker.task")

MAX_FACES = 2
WINDOW = "Face Tracker"

# 종료 키: q, Q, ESC(27). 한글 입력 상태에서는 q가 'ㅂ'으로 들어가므로 ESC도 받는다
QUIT_KEYS = (ord("q"), ord("Q"), 27)

C = vision.FaceLandmarksConnections

# (화면에 표시할 이름, 연결선 목록, 색(BGR), 선 두께)
PARTS = [
    ("Face oval", C.FACE_LANDMARKS_FACE_OVAL,     (255, 255, 255), 2),  # 얼굴 윤곽: 흰색
    ("Eyebrows",  C.FACE_LANDMARKS_LEFT_EYEBROW,  (0, 165, 255),   2),  # 눈썹: 주황
    (None,        C.FACE_LANDMARKS_RIGHT_EYEBROW, (0, 165, 255),   2),
    ("Eyes",      C.FACE_LANDMARKS_LEFT_EYE,      (0, 255, 0),     2),  # 눈: 초록
    (None,        C.FACE_LANDMARKS_RIGHT_EYE,     (0, 255, 0),     2),
    ("Iris",      C.FACE_LANDMARKS_LEFT_IRIS,     (0, 255, 255),   1),  # 홍채: 노랑
    (None,        C.FACE_LANDMARKS_RIGHT_IRIS,    (0, 255, 255),   1),
    ("Nose",      C.FACE_LANDMARKS_NOSE,          (255, 128, 0),   2),  # 코: 파랑
    ("Lips",      C.FACE_LANDMARKS_LIPS,          (0, 0, 255),     2),  # 입술: 빨강
]
EAR_COLOR = (255, 100, 200)       # 귀(추정): 보라
EAR_HIDDEN_COLOR = (130, 130, 130)  # 가려진 귀: 회색

# 주요 지점의 특징점 번호 (MediaPipe 478점 기준)
NOSE_TIP = 1
LEFT_IRIS_CENTER = 473
RIGHT_IRIS_CENTER = 468
MOUTH_TOP, MOUTH_BOTTOM = 13, 14
EYE_INNER = (133, 362)        # 두 눈의 안쪽 끝 (안경 브리지가 이 사이에 있다)
FACE_SIDES = (234, 454)       # 얼굴 윤곽의 양 끝 = 귀 바로 앞

# 안경 판별: 브리지 영역에서 강한 가로 경계선이 지나가는 열의 비율 (0~1)
# 실측(40초, 안경 썼다 벗었다): 안경 벗음 0.00~0.16 / 안경 씀 대부분 0.9 이상,
#                               고개를 돌리면 0.4대까지 떨어짐
# 켜짐/꺼짐 기준을 다르게 두어(히스테리시스) 기준 근처에서 YES/NO가 깜빡이지 않게 한다
GLASSES_ON = 0.4              # NO → YES 로 바뀌는 점수
GLASSES_OFF = 0.15            # YES → NO 로 바뀌는 점수
GLASSES_SMOOTH = 0.9          # 이동 평균에서 이전 값의 비중 (클수록 안정적, 약간 느림)
EDGE_STRENGTH = 200           # 이 값보다 강한 경계만 "선"으로 본다

# 고개 방향: 코끝이 얼굴 양 끝 사이 어디에 있는지 (0=왼쪽 끝, 0.5=정면, 1=오른쪽 끝)
EAR_HIDDEN_RATIO = 0.2        # 코끝이 한쪽 끝에서 20% 이내로 붙으면 그쪽 귀는 얼굴 뒤로 가려짐


def ensure_model():
    """모델 파일이 없으면 내려받는다 (처음 한 번만, 약 3.6MB)."""
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("얼굴 특징점 모델 다운로드 중...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def glasses_score(gray, pts):
    """두 눈 사이(안경 브리지 위치)에 가로 경계선이 얼마나 걸쳐 있는지 0~1로 돌려준다."""
    a, b = pts[EYE_INNER[0]], pts[EYE_INNER[1]]
    x1, x2 = sorted((a[0], b[0]))
    yc = (a[1] + b[1]) // 2
    eye_dist = np.hypot(pts[LEFT_IRIS_CENTER][0] - pts[RIGHT_IRIS_CENTER][0],
                        pts[LEFT_IRIS_CENTER][1] - pts[RIGHT_IRIS_CENTER][1])
    hh = max(int(eye_dist * 0.35), 6)
    y1, y2 = yc - hh, yc + int(hh * 0.3)

    patch = gray[max(y1, 0):max(y2, 0), max(x1, 0):max(x2, 0)].astype(np.float32)
    if patch.shape[0] < 4 or patch.shape[1] < 5:
        return None  # 영역이 너무 작으면 판단하지 않음

    # 세로 방향 밝기 변화(Sobel y) = 가로로 놓인 경계선
    edge = np.abs(cv2.Sobel(patch, cv2.CV_32F, 0, 1, ksize=3))
    # 각 열(세로줄)마다 강한 가로 경계가 하나라도 있으면 "선이 지나감"
    return float((edge > EDGE_STRENGTH).any(axis=0).mean())


def estimate_ears(pts):
    """얼굴 윤곽 양 끝을 기준으로 귀 위치(타원)와 보임 여부를 추정한다.

    화면이 거울 모드이므로 화면 왼쪽 = 본인의 왼쪽이다.
    반환: [(이름, 중심, 반지름(가로, 세로), 보이는지), ...]
    """
    side_a, side_b = pts[FACE_SIDES[0]], pts[FACE_SIDES[1]]
    left, right = sorted((side_a, side_b), key=lambda p: p[0])
    nose = pts[NOSE_TIP]

    # 고개 방향: 코끝이 오른쪽 끝에 가까우면 오른쪽 귀가 얼굴 뒤로 가려진다
    width = max(right[0] - left[0], 1)
    ratio = (nose[0] - left[0]) / width

    # 귀 높이: 눈 높이 조금 위 ~ 코끝 조금 아래
    eye_y = (pts[LEFT_IRIS_CENTER][1] + pts[RIGHT_IRIS_CENTER][1]) / 2
    span = max(nose[1] - eye_y, 10)
    top, bottom = eye_y - 0.35 * span, nose[1] + 0.35 * span
    ry = (bottom - top) / 2
    rx = ry * 0.45
    cy = int((top + bottom) / 2)

    ears = []
    for name, edge, outward, visible in (
        ("L ear", left, -1, ratio > EAR_HIDDEN_RATIO),
        ("R ear", right, +1, ratio < 1 - EAR_HIDDEN_RATIO),
    ):
        cx = int(edge[0] + outward * rx)  # 윤곽 끝에서 바깥쪽으로 귀 반 폭만큼
        ears.append((name, (cx, cy), (int(rx), int(ry)), visible))
    return ears


def update_glasses(state, score):
    """안경 상태 갱신. state = {"avg": 점수 평균, "on": 착용 여부}"""
    if score is None:
        return state
    if state["avg"] is None:
        state["avg"] = score
        state["on"] = score >= GLASSES_ON
        return state
    state["avg"] = GLASSES_SMOOTH * state["avg"] + (1 - GLASSES_SMOOTH) * score
    if not state["on"] and state["avg"] >= GLASSES_ON:
        state["on"] = True
    elif state["on"] and state["avg"] < GLASSES_OFF:
        state["on"] = False
    return state


def draw_face(frame, landmarks, face_no, show_mesh=False, glasses=None):
    """glasses: update_glasses()가 돌려준 상태 (없으면 None)"""
    """특징점 목록을 받아 프레임 위에 얼굴 부위를 그리고, 코끝 좌표를 돌려준다."""
    h, w = frame.shape[:2]
    # 특징점 좌표는 0~1 비율 → 픽셀 좌표로 변환
    pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]

    if show_mesh:
        for c in C.FACE_LANDMARKS_TESSELATION:
            cv2.line(frame, pts[c.start], pts[c.end], (80, 80, 80), 1, cv2.LINE_AA)

    for _, connections, color, thickness in PARTS:
        for c in connections:
            cv2.line(frame, pts[c.start], pts[c.end], color, thickness, cv2.LINE_AA)

    # 주요 지점: 두 눈동자 중심, 코끝, 입 중앙
    mouth = ((pts[MOUTH_TOP][0] + pts[MOUTH_BOTTOM][0]) // 2,
             (pts[MOUTH_TOP][1] + pts[MOUTH_BOTTOM][1]) // 2)
    for p in (pts[LEFT_IRIS_CENTER], pts[RIGHT_IRIS_CENTER], pts[NOSE_TIP], mouth):
        cv2.circle(frame, p, 4, (255, 0, 255), -1, cv2.LINE_AA)

    # 귀 (추정 위치)
    ears = estimate_ears(pts)
    for name, center, axes, visible in ears:
        color = EAR_COLOR if visible else EAR_HIDDEN_COLOR
        cv2.ellipse(frame, center, axes, 0, 0, 360, color, 2 if visible else 1, cv2.LINE_AA)
        cv2.putText(frame, name, (center[0] - axes[0], center[1] - axes[1] - 5),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)

    # 특징점 전체를 감싸는 사각형 = 얼굴 검출 영역
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x1, y1, x2, y2 = min(xs), min(ys), max(xs), max(ys)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
    cv2.putText(frame, f"Face {face_no}", (x1, max(y1 - 8, 15)),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # 얼굴 아래에 안경 / 귀 정보 출력
    if glasses is None or glasses["avg"] is None:
        glasses_text = "Glasses: ?"
    else:
        glasses_text = f"Glasses: {'YES' if glasses['on'] else 'NO'} ({glasses['avg']:.2f})"
    ears_text = "Ears: " + ", ".join(f"{n.split()[0]} {'visible' if v else 'hidden'}"
                                     for n, _, _, v in ears)
    for i, text in enumerate((glasses_text, ears_text)):
        y = min(y2 + 20 + i * 20, h - 5 - (1 - i) * 20)
        cv2.putText(frame, text, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 0), 4)
        cv2.putText(frame, text, (x1, y), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 1)

    return pts[NOSE_TIP], pts


def draw_legend(frame, fps, face_count):
    # 밝은 배경에서도 글자가 보이도록 반투명 어두운 바탕
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (255, 215), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)

    cv2.putText(frame, f"FPS {fps:.0f}  Faces {face_count}", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    y = 50
    legend = [(name, color) for name, _, color, _ in PARTS if name] + [("Ears (estimated)", EAR_COLOR)]
    for name, color in legend:
        cv2.rectangle(frame, (10, y - 10), (24, y + 2), color, -1)
        cv2.putText(frame, name, (30, y), cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1)
        y += 20
    cv2.putText(frame, "q/ESC:quit m:mesh t:trail", (10, y + 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 200, 200), 1)


def create_landmarker():
    ensure_model()
    options = vision.FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,  # 연속 프레임: 이전 결과로 추적
        num_faces=MAX_FACES,
        # 기본값(0.5)보다 낮춰서 고개를 숙이거나 돌린 얼굴도 놓치지 않게 한다
        min_face_detection_confidence=0.3,
        min_face_presence_confidence=0.3,
        min_tracking_confidence=0.3,
    )
    return vision.FaceLandmarker.create_from_options(options)


def main():
    cap = cv2.VideoCapture(0)
    trails = [deque(maxlen=40) for _ in range(MAX_FACES)]  # 얼굴별 코끝 이동 경로

    try:
        run_loop(cap, trails)
    except KeyboardInterrupt:  # 터미널에서 Ctrl+C
        pass
    finally:
        # 어떻게 종료하든 카메라와 창은 반드시 정리
        cap.release()
        cv2.destroyAllWindows()
        print("종료합니다.")


def run_loop(cap, trails):
    show_mesh, show_trail = False, True
    last_ts, prev_time, fps = -1, time.time(), 0.0
    # 얼굴별 안경 상태 (점수 이동 평균 + 착용 여부)
    glasses = [{"avg": None, "on": False} for _ in range(MAX_FACES)]

    with create_landmarker() as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("웹캠을 읽을 수 없습니다.")
                break

            frame = cv2.flip(frame, 1)  # 거울 모드
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 안경 판별용 (그리기 전 원본)

            # OpenCV(BGR) → MediaPipe(RGB) 이미지로 변환
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb)

            # VIDEO 모드는 타임스탬프(ms)가 계속 증가해야 한다
            ts = max(int(time.time() * 1000), last_ts + 1)
            last_ts = ts
            result = landmarker.detect_for_video(image, ts)

            faces = result.face_landmarks
            h, w = frame.shape[:2]
            for i, landmarks in enumerate(faces):
                # 안경: 이번 프레임 점수로 상태 갱신
                pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]
                update_glasses(glasses[i], glasses_score(gray, pts))

                nose, _ = draw_face(frame, landmarks, i + 1, show_mesh, glasses[i])
                trails[i].append(nose)
            for i in range(len(faces), MAX_FACES):
                trails[i].clear()       # 사라진 얼굴의 경로와 안경 상태는 지움
                glasses[i] = {"avg": None, "on": False}

            if show_trail:
                for trail in trails:
                    for a, b in zip(trail, list(trail)[1:]):
                        cv2.line(frame, a, b, (255, 0, 255), 2, cv2.LINE_AA)

            now = time.time()
            fps = 0.9 * fps + 0.1 * (1 / max(now - prev_time, 1e-6))
            prev_time = now
            draw_legend(frame, fps, len(faces))

            cv2.imshow(WINDOW, frame)
            key = cv2.waitKey(1) & 0xFF
            if key in QUIT_KEYS:
                break
            if key == ord("m"):
                show_mesh = not show_mesh
            if key == ord("t"):
                show_trail = not show_trail

            # 창의 X 버튼으로 닫았는지 확인 (확인하지 않으면 imshow가 창을 다시 띄운다)
            if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                break


if __name__ == "__main__":
    main()
