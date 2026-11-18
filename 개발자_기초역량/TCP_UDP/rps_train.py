"""
가위바위보 분류기 학습

rps_collect.py 로 모은 관절 좌표(data/rps_landmarks.csv)로 분류기를 학습해서
models/rps_classifier.joblib 로 저장한다. 저장된 모델이 있으면 rps_detector.py 가 자동으로 사용한다.

정확도 측정 방법:
  같은 모양을 연속으로 찍은 프레임들은 서로 거의 똑같다. 무작위로 나누면 "거의 같은 사진"이
  학습과 시험에 동시에 들어가서 정확도가 부풀려진다.
  그래서 모양마다 앞쪽 80%로 학습하고, 나중에 찍은 뒤쪽 20%로 시험한다.

실행: python rps_train.py
"""

import csv
import os

import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

import rps_detector as rps

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE, "data", "rps_landmarks.csv")
MODEL_PATH = os.path.join(BASE, "models", "rps_classifier.joblib")
TEST_RATIO = 0.2


def load():
    by_label = {}
    with open(DATA_PATH, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            xyz = [float(row[f"{a}{i}"]) for i in range(21) for a in "xyz"]
            feat = rps.landmark_features(xyz, row["handedness"])
            by_label.setdefault(row["label"], []).append(feat)
    return by_label


def split(by_label):
    Xtr, ytr, Xte, yte = [], [], [], []
    for label, feats in by_label.items():
        n_test = max(int(len(feats) * TEST_RATIO), 1)
        Xtr += feats[:-n_test]; ytr += [label] * (len(feats) - n_test)
        Xte += feats[-n_test:]; yte += [label] * n_test
    return np.array(Xtr), np.array(ytr), np.array(Xte), np.array(yte)


def main():
    by_label = load()
    print("샘플 수:", {k: len(v) for k, v in by_label.items()})
    missing = [c for c in ("ROCK", "SCISSORS", "PAPER", "NONE") if c not in by_label]
    if missing:
        print("경고: 데이터가 없는 모양:", missing)

    Xtr, ytr, Xte, yte = split(by_label)

    candidates = {
        "k-NN": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=7)),
        "RandomForest": RandomForestClassifier(n_estimators=200, random_state=0),
        "MLP": make_pipeline(StandardScaler(),
                             MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=2000, random_state=0)),
    }
    best_name, best_model, best_acc = None, None, -1
    for name, model in candidates.items():
        model.fit(Xtr, ytr)
        acc = (model.predict(Xte) == yte).mean()
        print(f"{name:13s} 시험 정확도 {acc * 100:5.1f}%")
        if acc > best_acc:
            best_name, best_model, best_acc = name, model, acc

    print(f"\n선택: {best_name}")
    pred = best_model.predict(Xte)
    labels = sorted(set(yte))
    print(classification_report(yte, pred, labels=labels, zero_division=0))
    print("혼동 행렬 (행=정답, 열=예측):", labels)
    print(confusion_matrix(yte, pred, labels=labels))

    # 최종 모델은 모든 데이터로 다시 학습해서 저장
    X = np.vstack([Xtr, Xte]); y = np.concatenate([ytr, yte])
    best_model.fit(X, y)
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    joblib.dump(best_model, MODEL_PATH)
    print("저장:", MODEL_PATH)


if __name__ == "__main__":
    main()
