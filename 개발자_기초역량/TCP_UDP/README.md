# TCP와 UDP 네트워크 실습

Python 표준 라이브러리와 OpenCV/MediaPipe를 활용해 TCP 및 UDP 통신을 단계적으로 실습하는 예제 모음입니다.

> 이 폴더는 [AX 서비스 풀스택 빌더 과정](../../)의 개발자 기초 역량 중 네트워크와 실시간 데이터 전송 내용을 다룹니다.

## 학습 구성

- **TCP 기초**: 연결 지향 통신과 Echo 서버/클라이언트
- **TCP 멀티 채팅**: 다중 클라이언트를 스레드로 처리하고 메시지 브로드캐스트
- **TCP 1:1 메시지**: 지정된 사용자 간 대화와 오프라인 메시지 보관
- **UDP 웹캠**: 신뢰성보다 실시간성을 중시하는 UDP 프레임 송수신
- **MediaPipe 응용**: 웹캠으로 손짓과 얼굴 특징을 실시간 분석
- **머신러닝 응용**: 가위바위보 관절 데이터를 수집하고 분류기를 학습

## 파일 구성

| 파일 | 설명 |
|---|---|
| `tcp_server.py` | 단일 클라이언트가 보낸 데이터를 Echo로 반환하는 TCP 서버 |
| `tcp_client.py` | TCP 서버에 데이터를 송신하는 기본 클라이언트 |
| `tcp_chat_server.py` | 여러 클라이언트를 스레드로 처리하는 TCP 채팅 서버 |
| `tcp_chat_client.py` | 멀티 채팅 서버에 접속하는 클라이언트 |
| `dm_server.py` | Alice-Bob 1:1 대화 중계 서버; 오프라인 메시지와 접속 상태 관리 |
| `dm_client.py` | 지정한 사용자로 로그인하여 1:1 대화 |
| `simple_http_server.py` | 표준 라이브러리로 동작하는 간단한 HTTP 서버 |
| `udp_webcam_server.py` | 웹캠 JPEG 프레임을 UDP로 다수의 수강생에게 송신 |
| `udp_webcam_client.py` | UDP 웹캠 프레임을 수신하고 화면에 출력 |
| `rps_collect.py` | 가위바위보 손 관절 데이터를 수집하여 CSV로 저장 |
| `rps_train.py` | 수집된 관절 데이터로 분류기를 학습하고 최적 모델 저장 |
| `rps_detector.py` | 웹캠 손 관절을 분석하여 바위/가위/보를 실시간 판정 |
| `face_tracker.py` | 얼굴 특징점, 안경 착용 여부, 귀 위치 추정 및 코끝 추적 |
| `train_tuning.md` | 가위바위보 분류기 튜닝 실험 및 결과 정리 |
| `udp_useCaseDiagram.md` | UDP 웹캠 및 관련 사용 사례 다이어그램 |
| `udp_userStory.md` | UDP 웹캠 기능의 사용자 스토리 |
| `webcam_viewer.md` | 웹캠 뷰어 구현 설명 |
| `data/rps_landmarks.csv` | 손 관절 좌표 학습 데이터 |
| `models/` | MediaPipe 모델 및 가위바위보 분류기 저장 경로 |

## 사전 준비

Python 3가 필요합니다.

```bash
# 기본 실습에는 추가 패키지 없이 Python 표준 라이브러리를 사용할 수 있습니다.

# 웹캠 및 MediaPipe 실습용 패키지
pip install opencv-python mediapipe

# 가위바위보 분류기 학습용 패키지
pip install numpy scikit-learn joblib
```

MediaPipe의 다음 모델 파일이 없으면 예제 실행 시 자동으로 다운로드됩니다.

- `models/hand_landmarker.task`
- `models/face_landmarker.task`

모델은 약 수십 MB까지 포함될 수 있으므로 최초 실행 후 네트워크 연결이 필요할 수 있습니다.

## 실행 예제

### 1. 기본 TCP Echo

터미널 1에서 서버를 실행합니다.

```bash
python tcp_server.py
```

터미널 2에서 별도 클라이언트를 실행할 수 있습니다. 기본 TCP 클라이언트는 현재 대화형 입력을 제공하지 않으므로 별도 Python 코드에서 서버의 `5000` 포트로 접속하거나 다음 구성의 멀티 채팅 예제를 사용하세요.

### 2. TCP 멀티 채팅

```bash
python tcp_chat_server.py
```

다른 터미널에서 각 사용자별로 클라이언트를 실행합니다.

```bash
python tcp_chat_client.py
```

- 서버 포트: `5001`
- 기본 주소: `127.0.0.1`
- 종료: 클라이언트에서 `exit`

### 3. TCP 1:1 메시지

먼저 DM 서버를 실행합니다.

```bash
python dm_server.py
```

Alice와 Bob을 각각 다른 터미널에서 실행합니다.

```bash
python dm_client.py alice
python dm_client.py bob
```

- 서버 포트: `5002`
- 대화 상대는 서버의 `PARTNERS` 설정에 따라 고정됩니다.
- 상대가 오프라인이면 서버가 메시지를 보관한 후 로그인 시 전달합니다.
- 종료: `/exit`

### 4. HTTP 서버

```bash
python simple_http_server.py
```

실행 후 브라우저 또는 `curl`로 서버 주소에 접속하면 간단한 응답을 확인할 수 있습니다.

### 5. UDP 웹캠 송수신

강사 또는 송신 측에서 서버를 실행합니다.

```bash
python udp_webcam_server.py
```

수강생 또는 수신 측에서 실행합니다.

```bash
python udp_webcam_client.py
```

다른 PC에서 수신하려면 서버의 IP 주소를 인자로 전달합니다.

```bash
python udp_webcam_client.py <서버_IP>
```

- UDP 포트: `6000`
- 프레임 크기: `640 x 480`
- JPEG 품질: `50`
- 송신 측에서는 `q`, 수신 측에서도 `q`로 종료합니다.
- UDP는 수신 확인을 하지 않으므로 프레임이 일부 누락될 수 있습니다.

### 6. 가위바위보 인식

바로 규칙 기반으로 인식합니다.

```bash
python rps_detector.py
```

학습 데이터를 추가로 수집합니다.

```bash
python rps_collect.py
```

특정 클래스만 추가 수집할 수도 있습니다.

```bash
python rps_collect.py ROCK
python rps_collect.py ROCK PAPER
python rps_collect.py NONE
```

수집이 끝난 뒤 분류기를 학습합니다.

```bash
python rps_train.py
```

학습 결과로 `models/rps_classifier.joblib`이 생성됩니다. 이 모델을 사용하려면 `rps_detector.py`의 `USE_MODEL`을 `True`로 설정합니다.

- 기본 판정 방식: 손가락 펴짐 규칙
- 바위: 검지~새끼가 모두 접힘
- 가위: 펴진 손가락이 총 2개
- 보: 펴진 손가락이 4개 이상
- 펴진 손가락이 1개 또는 3개인 경우는 미판정
- 최근 프레임의 다수결로 판정을 안정화

### 7. 얼굴 추적

```bash
python face_tracker.py
```

- `m`: 얼굴 메쉬 표시 전환
- `t`: 코끝 이동 경로 표시 전환
- `q`, `Q`, `Esc`: 종료
- 최대 2명까지 동시에 인식

## TCP와 UDP의 차이

| 항목 | TCP | UDP |
|---|---|---|
| 연결 방식 | 연결 지향 | 비연결 |
| 데이터 전달 | 순서 보장, 재전송 | 순서/손실 보장 없음 |
| 적합한 용도 | 채팅, 파일 전송, 인증 등 정확한 전달이 필요한 작업 | 영상 스트리밍, 센서 데이터 등 실시간성이 중요한 작업 |
| 이 폴더의 예제 | Echo, 채팅, 1:1 메시지 | 웹캠 프레임 송수신 |

## 권장 실습 순서

1. `tcp_server.py`와 `tcp_client.py`로 기본 Echo 통신 이해
2. `tcp_chat_server.py`와 `tcp_chat_client.py`로 스레드 기반 다중 접속 실습
3. `dm_server.py`와 `dm_client.py`로 JSON 프로토콜과 오프라인 메시지 구현 이해
4. `udp_webcam_server.py`와 `udp_webcam_client.py`로 UDP 프레임 전송 체험
5. `rps_collect.py`와 `rps_train.py`로 데이터 수집 및 분류 학습 실습
6. `rps_detector.py`와 `face_tracker.py`로 실시간 MediaPipe 응용 실습

## 주의사항

- 기본 예제의 주소와 포트는 로컬 호스트 기준입니다.
- 여러 터미널에서 실행할 때 포트 중복을 피하세요.
  - TCP Echo: `5000`
  - TCP 채팅: `5001`
  - 1:1 메시지: `5002`
  - UDP 웹캠: `6000`
- 방화벽이나 공유기 설정에 따라 다른 PC 간 UDP 통신이 제한될 수 있습니다.
- 웹캠 예제는 카메라 장치가 하나 이상 연결된 환경이 필요합니다.
- 서버 종료는 터미널의 `Ctrl+C` 또는 예제 창의 `q`/`Esc`를 사용합니다.
