"""
웹캠 가위바위보 검출 (MediaPipe Hand Landmarker)

1) 손 하나당 21개의 관절 위치(landmark)를 찾는다.
2) 손가락마다 "펴짐 / 접힘"을 판단한다.
   - 3D 관절 좌표로 손가락이 굽은 각도를 구해서, 100도 미만이면 펴진 것
     (각도라서 손을 기울이거나 손가락이 카메라 쪽을 향해도 판단할 수 있음)
3) 엄지를 포함한 펴진 손가락 수로 판정한다.
   - 바위: 검지~새끼 모두 접힘 (엄지를 세운 주먹도 바위)
   - 가위: 정확히 2개 (V, L자, 엄지+새끼 등 어느 손가락이든)
   - 보  : 4개 이상
   - 1개, 3개는 무시한다 (판정 결과를 표시하지 않음)
4) 최근 몇 프레임의 결과로 다수결을 해서 판정이 깜빡이지 않게 한다.

        손 관절 번호 (MediaPipe)
              8   12  16  20      ← 손가락 끝(tip)
              7   11  15  19
         4    6   10  14  18      ← 가운데 마디(PIP)
         3    5    9  13  17      ← 손가락 뿌리(MCP)
          2
           1        0             ← 손목(wrist)

준비: pip install mediapipe opencv-python
실행: python rps_detector.py
키:   q 또는 ESC 종료 (창의 X 버튼, 터미널 Ctrl+C로도 종료)
"""

import os
import time
import urllib.request
from collections import Counter, deque

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks.python import BaseOptions, vision

MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "hand_landmarker.task")
MODEL_URL = ("https://storage.googleapis.com/mediapipe-models/"
             "hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task")

CLASSIFIER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", "rps_classifier.joblib")
MIN_CONFIDENCE = 0.6                   # 학습 모델이 이보다 확신이 낮으면 판정하지 않음
# 학습 모델 사용 여부. 기본은 개수 규칙(가위 2개, 보 4개)으로 판정한다.
# 학습 데이터가 규칙과 정확히 같은 기준으로 수집됐을 때만 True 로 바꿔서 쓴다.
USE_MODEL = False

# 손가락이 "펴짐"으로 판정되는 최대 굽은 각도 (손목-뿌리-마디-마디-끝, 꺾인 각도의 합)
# 수집 데이터 실측: 보 평균 약 30도, 바위 평균 약 210도
BEND_LIMIT = 100
# 엄지가 "펴짐"으로 판정되는 기준: 엄지 끝~중지 뿌리 거리 / 손바닥 길이(손목~중지 뿌리)
# 수집 데이터 실측: 접은 엄지(주먹, V 가위) 대부분 0.3~0.6 / 편 엄지(L 가위) 대부분 0.8 이상
THUMB_OUT_RATIO = 0.75
FINGER_JOINTS = {           # 손목 다음부터: 뿌리(MCP), 가운데 마디(PIP), 끝 마디(DIP), 끝(TIP)
    "Index":  (5, 6, 7, 8),
    "Middle": (9, 10, 11, 12),
    "Ring":   (13, 14, 15, 16),
    "Pinky":  (17, 18, 19, 20),
}

MAX_HANDS = 2
WINDOW = "Rock Paper Scissors"
QUIT_KEYS = (ord("q"), ord("Q"), 27)   # q, Q, ESC (한글 입력 상태 대비)
VOTE_FRAMES = 7                        # 다수결에 쓸 최근 프레임 수

WRIST = 0
# 손가락 이름: (끝, 가운데 마디) 관절 번호
FINGERS = {
    "Thumb":  (4, 3),
    "Index":  (8, 6),
    "Middle": (12, 10),
    "Ring":   (16, 14),
    "Pinky":  (20, 18),
}
PINKY_MCP = 17
MIDDLE_MCP = 9

GESTURES = {
    "ROCK":     ("바위", (0, 0, 255)),      # 빨강
    "SCISSORS": ("가위", (0, 200, 255)),    # 주황
    "PAPER":    ("보",   (0, 220, 0)),      # 초록
}
NO_RESULT_COLOR = (180, 180, 180)           # 아직 판정 전: 회색

HC = vision.HandLandmarksConnections


def ensure_model():
    """모델 파일이 없으면 내려받는다 (처음 한 번만, 약 7.8MB)."""
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("손 관절 모델 다운로드 중...")
        urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)


def landmark_features(xyz, side):
    """관절 좌표 21개(x, y, z) → 학습/판정용 특징 벡터 (63개 숫자).

    - 손목을 원점으로 옮긴다       → 화면 어디에 손이 있든 같은 값
    - 손 크기로 나눈다             → 카메라와의 거리에 상관없음
    - 오른손은 좌우를 뒤집는다     → 왼손/오른손을 같은 모양으로 취급
    """
    a = np.asarray(xyz, dtype=np.float32).reshape(21, 3).copy()
    a -= a[WRIST]
    if side == "Right":
        a[:, 0] = -a[:, 0]
    scale = np.linalg.norm(a[:, :2], axis=1).max()
    return (a / max(scale, 1e-6)).ravel()


def bend_angle(p, joints):
    """손가락이 굽은 정도(도). 손목→뿌리→마디→마디→끝 을 잇는 선이 꺾인 각도의 합.
    곧게 펴면 0도에 가깝고, 주먹을 쥐면 200도 이상이 된다."""
    chain = [p[WRIST]] + [p[j] for j in joints]
    total = 0.0
    for k in range(1, len(chain) - 1):
        v1, v2 = chain[k] - chain[k - 1], chain[k + 1] - chain[k]
        cos = v1 @ v2 / (np.linalg.norm(v1) * np.linalg.norm(v2) + 1e-9)
        total += np.degrees(np.arccos(np.clip(cos, -1, 1)))
    return total


def finger_states(landmarks, w, h):
    """손가락별 펴짐(True) / 접힘(False).

    3D 좌표(z 포함)로 관절 각도를 보기 때문에, 손가락이 카메라 쪽을 향해도 판단할 수 있다.
    """
    # 정규화 좌표 → 픽셀 비율에 맞춘 3D 좌표 (z는 x와 같은 스케일)
    p = np.array([[l.x * w, l.y * h, l.z * w] for l in landmarks])

    # 엄지: 손바닥 가운데(중지 뿌리)에서 엄지 끝이 충분히 멀면 펴진 것
    palm = np.linalg.norm(p[MIDDLE_MCP] - p[WRIST])
    states = {"Thumb": np.linalg.norm(p[4] - p[MIDDLE_MCP]) / max(palm, 1e-6) > THUMB_OUT_RATIO}
    for name, joints in FINGER_JOINTS.items():
        states[name] = bend_angle(p, joints) < BEND_LIMIT
    return states


def classify(states):
    """펴진 손가락 수 → ROCK / SCISSORS / PAPER / None(무시)"""
    four = sum([states["Index"], states["Middle"], states["Ring"], states["Pinky"]])  # 0~4
    total = four + states["Thumb"]                                                    # 엄지 포함 0~5

    if four == 0:
        return "ROCK"       # 검지~새끼 모두 접힘 (엄지를 세운 주먹도 바위)
    if total == 2:
        return "SCISSORS"   # 엄지 포함 정확히 2개 (V, L자, 엄지+새끼 등)
    if total >= 4:
        return "PAPER"      # 엄지 포함 4개 이상
    return None             # 1개 또는 3개 → 무시 (판정 결과 없음)


def load_classifier():
    """USE_MODEL 이 True 이고 rps_train.py 로 학습한 모델이 있으면 불러온다. 아니면 None (규칙으로 판정)."""
    if not USE_MODEL or not os.path.exists(CLASSIFIER_PATH):
        return None
    import joblib
    return joblib.load(CLASSIFIER_PATH)


def classify_ml(model, landmarks, side):
    """학습 모델로 판정 → ROCK / SCISSORS / PAPER / None(NONE이거나 확신 낮음)"""
    feat = landmark_features([v for p in landmarks for v in (p.x, p.y, p.z)], side)
    proba = model.predict_proba([feat])[0]
    best = int(np.argmax(proba))
    label = model.classes_[best]
    if label == "NONE" or proba[best] < MIN_CONFIDENCE:
        return None
    return label


def draw_hand(frame, pts, states, label, side):
    # 뼈대
    for c in HC.HAND_CONNECTIONS:
        cv2.line(frame, pts[c.start], pts[c.end], (255, 255, 255), 2, cv2.LINE_AA)
    for p in pts:
        cv2.circle(frame, p, 3, (80, 80, 80), -1, cv2.LINE_AA)

    # 손가락 끝: 펴짐 초록 / 접힘 빨강
    for name, (tip, _) in FINGERS.items():
        color = (0, 220, 0) if states[name] else (0, 0, 255)
        cv2.circle(frame, pts[tip], 8, color, -1, cv2.LINE_AA)

    # 손 영역과 판정 결과
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    x1, y1, x2, y2 = min(xs) - 15, min(ys) - 15, max(xs) + 15, max(ys) + 15
    color = GESTURES[label][1] if label else NO_RESULT_COLOR
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
    text = f"{side}: {label}" if label else side
    cv2.putText(frame, text, (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 5)
    cv2.putText(frame, text, (x1, max(y1 - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    # 손 아래에 손가락 머리글자 T I M R P (엄지~새끼): 펴짐 초록 / 접힘 빨강
    x = x1
    for name in FINGERS:
        c = (0, 220, 0) if states[name] else (0, 0, 255)
        cv2.putText(frame, name[0], (x, y2 + 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, c, 2)
        x += 20


def draw_info(frame, fps, hand_count, mode):
    overlay = frame.copy()
    cv2.rectangle(overlay, (0, 0), (300, 95), (0, 0, 0), -1)
    cv2.addWeighted(overlay, 0.5, frame, 0.5, 0, frame)
    cv2.putText(frame, f"FPS {fps:.0f}  Hands {hand_count}  [{mode}]", (10, 25),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "finger tip: green=open red=closed", (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)
    cv2.putText(frame, "q/ESC: quit", (10, 75),
                cv2.FONT_HERSHEY_SIMPLEX, 0.45, (220, 220, 220), 1)


def create_landmarker():
    ensure_model()
    options = vision.HandLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=MODEL_PATH),
        running_mode=vision.RunningMode.VIDEO,  # 연속 프레임: 이전 결과로 추적
        num_hands=MAX_HANDS,
    )
    return vision.HandLandmarker.create_from_options(options)


def run_loop(cap):
    votes = {}          # "Left"/"Right" → 최근 판정 기록
    shown = {}          # 콘솔에 마지막으로 출력한 판정
    last_ts, prev_time, fps = -1, time.time(), 0.0

    model = load_classifier()
    mode = "model" if model is not None else "rule"
    print("판정 방식:", "학습 모델 (" + CLASSIFIER_PATH + ")" if model is not None else "손가락 개수 규칙")

    with create_landmarker() as landmarker:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("웹캠을 읽을 수 없습니다.")
                break

            frame = cv2.flip(frame, 1)  # 거울 모드 (MediaPipe의 왼손/오른손 판정도 거울 기준)
            image = mp.Image(image_format=mp.ImageFormat.SRGB,
                             data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            ts = max(int(time.time() * 1000), last_ts + 1)  # VIDEO 모드: 증가하는 타임스탬프
            last_ts = ts
            result = landmarker.detect_for_video(image, ts)

            h, w = frame.shape[:2]
            seen = set()
            for landmarks, handed in zip(result.hand_landmarks, result.handedness):
                side = handed[0].category_name          # "Left" / "Right"
                pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]

                states = finger_states(landmarks, w, h)
                vote = votes.setdefault(side, deque(maxlen=VOTE_FRAMES))
                # 1개·3개(None)도 "무시" 한 표로 넣는다.
                # 다수결이 None이면 결과를 표시하지 않고, 손을 바꾸는 순간의 한두 프레임은 무시된다
                if model is not None:
                    vote.append(classify_ml(model, landmarks, side))
                else:
                    vote.append(classify(states))
                label = Counter(vote).most_common(1)[0][0]   # 다수결

                draw_hand(frame, pts, states, label, side)
                seen.add(side)

                # 판정이 바뀌었을 때만 콘솔에 한글로 출력
                if shown.get(side) != label:
                    shown[side] = label
                    if label:
                        print(f"{'왼손' if side == 'Left' else '오른손'}: {GESTURES[label][0]}")

            for side in list(votes):
                if side not in seen:     # 화면에서 사라진 손은 기록 초기화
                    votes.pop(side)
                    shown.pop(side, None)

            now = time.time()
            fps = 0.9 * fps + 0.1 * (1 / max(now - prev_time, 1e-6))
            prev_time = now
            draw_info(frame, fps, len(result.hand_landmarks), mode)

            cv2.imshow(WINDOW, frame)
            if (cv2.waitKey(1) & 0xFF) in QUIT_KEYS:
                break
            if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:   # X 버튼
                break


def main():
    cap = cv2.VideoCapture(0)
    try:
        run_loop(cap)
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("종료합니다.")


if __name__ == "__main__":
    main()
