"""
가위바위보 학습 데이터 수집 도구

화면 안내에 따라 손 모양을 보여주면, 손이 보이는 동안 관절 좌표(21개)를 계속 기록한다.
한 모양을 다 보여줬으면 Space 를 눌러 다음 모양으로 넘어간다.

  순서: SCISSORS(가위) → ROCK(바위) → PAPER(보) → NONE(무시: 1개, 3개, OK 사인 등)

  - 인정하고 싶은 모양을 "모두" 보여준다. (예: 가위는 V, 손가락 붙인 2개, 약지+새끼 ...)
  - 손 각도, 거리, 왼손/오른손을 바꿔 가며 보여주면 더 잘 학습된다.
  - Space 를 누른 직후 2초는 손을 바꾸는 시간이라 기록하지 않는다.

저장: data/rps_landmarks.csv  (실행할 때마다 이어서 추가)
실행: python rps_collect.py            (4가지 모두)
      python rps_collect.py NONE       (특정 모양만 추가 수집)
키:   Space 다음 모양 (준비 시간 2초 동안은 무시) / q·ESC 저장하고 종료
"""

import csv
import os
import time

import cv2
import mediapipe as mp

import rps_detector as rps

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "rps_landmarks.csv")

CLASSES = [
    ("SCISSORS", "show EVERY scissors shape you accept (2 fingers)"),
    ("ROCK",     "show fist in many angles"),
    ("PAPER",    "show open hand in many angles"),
    ("NONE",     "show shapes to IGNORE: 1 finger, 3 fingers, OK sign..."),
]
PREP_SECONDS = 2.0     # 다음 모양으로 넘어간 뒤 기록하지 않는 시간
WINDOW = "RPS Data Collect"


def main(only=None):
    classes = [c for c in CLASSES if only is None or c[0] in only]
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    new_file = not os.path.exists(DATA_PATH)
    f = open(DATA_PATH, "a", newline="", encoding="utf-8")
    writer = csv.writer(f)
    if new_file:
        header = ["label", "handedness"] + [f"{a}{i}" for i in range(21) for a in "xyz"]
        writer.writerow(header)

    cap = cv2.VideoCapture(0)
    counts = {name: 0 for name, _ in classes}
    idx, class_start, last_ts = 0, time.time(), -1

    try:
        with rps.create_landmarker() as landmarker:
            while idx < len(classes):
                ok, frame = cap.read()
                if not ok:
                    print("웹캠을 읽을 수 없습니다.")
                    break
                frame = cv2.flip(frame, 1)
                h, w = frame.shape[:2]
                image = mp.Image(image_format=mp.ImageFormat.SRGB,
                                 data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                ts = max(int(time.time() * 1000), last_ts + 1)
                last_ts = ts
                result = landmarker.detect_for_video(image, ts)

                name, hint = classes[idx]
                recording = time.time() - class_start >= PREP_SECONDS

                for landmarks, handed in zip(result.hand_landmarks, result.handedness):
                    pts = [(int(p.x * w), int(p.y * h)) for p in landmarks]
                    for c in rps.HC.HAND_CONNECTIONS:
                        cv2.line(frame, pts[c.start], pts[c.end], (255, 255, 255), 2, cv2.LINE_AA)
                    if recording:
                        row = [name, handed[0].category_name]
                        for p in landmarks:
                            row += [f"{p.x:.5f}", f"{p.y:.5f}", f"{p.z:.5f}"]
                        writer.writerow(row)
                        counts[name] += 1

                # 안내 화면
                cv2.rectangle(frame, (0, 0), (w, 90), (0, 0, 0), -1)
                cv2.putText(frame, f"[{idx + 1}/{len(classes)}] {name}", (10, 32),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 255), 2)
                cv2.putText(frame, hint, (10, 58), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                if recording:
                    status, color = f"REC  samples: {counts[name]}   SPACE = next", (0, 0, 255)
                else:
                    status = f"get ready... {PREP_SECONDS - (time.time() - class_start):.1f}s"
                    color = (0, 200, 255)
                cv2.putText(frame, status, (10, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.55, color, 2)
                if recording and not result.hand_landmarks:
                    cv2.putText(frame, "no hand", (w - 120, 82), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 0, 255), 2)

                cv2.imshow(WINDOW, frame)
                key = cv2.waitKey(1) & 0xFF
                # 준비 시간 중의 Space는 무시 (실수로 두 번 눌러 다음 모양을 건너뛰는 것 방지)
                if key == ord(" ") and recording:
                    print(f"{name}: {counts[name]}개 기록")
                    idx += 1
                    class_start = time.time()
                elif key in rps.QUIT_KEYS:
                    break
                if cv2.getWindowProperty(WINDOW, cv2.WND_PROP_VISIBLE) < 1:
                    break
    except KeyboardInterrupt:
        pass
    finally:
        cap.release()
        cv2.destroyAllWindows()
        f.close()
        print("저장:", DATA_PATH)
        print("이번에 기록한 샘플:", counts)


if __name__ == "__main__":
    import sys
    # 예: python rps_collect.py NONE        → NONE만 수집
    #     python rps_collect.py ROCK PAPER  → 바위, 보만 수집
    main([a.upper() for a in sys.argv[1:]] or None)
