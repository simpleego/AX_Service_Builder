# FastAPI 쿠키 & 세션 인증 실습 (백엔드 전용)

JWT 수업 전에 **쿠키 인증 → 서명 쿠키 → 서버 세션 인증**을 차례로 실습하며
"로그인 상태를 어디에, 어떻게 보관하는가"를 비교합니다. 프론트엔드 없이
Swagger UI, `requests.http`, 데모 스크립트로 테스트합니다.

## 1. 폴더 구조

```
웹인증/
├─ app/
│  ├─ main.py               # FastAPI 앱, 라우터 등록, 시작 시 테이블 생성
│  ├─ config.py             # .env 설정 로드
│  ├─ database.py           # SQLAlchemy 엔진/DB 세션 (MySQL + PyMySQL)
│  ├─ models.py             # users, login_sessions 테이블
│  ├─ schemas.py            # Pydantic 요청/응답 모델
│  ├─ security.py           # bcrypt 비밀번호 해시
│  └─ routers/
│     ├─ users.py           # [0] 회원가입 + 공통 로그인 검증
│     ├─ cookie_auth.py     # [1] 평문 쿠키(v1) / 서명 쿠키(v2)
│     └─ session_auth.py    # [2] DB 기반 서버 세션
├─ sql/schema.sql           # DB·계정·테이블 생성 스크립트
├─ scripts/demo_client.py   # 전체 시나리오 자동 실행 (공격 시나리오 포함)
├─ requests.http            # VS Code REST Client용 요청 모음
├─ requirements.txt
└─ .env.example
```

## 2. 실행 방법

```bash
# 1) 가상환경 + 패키지 설치
python -m venv venv
venv\Scripts\activate            # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

# 2) MySQL에 DB/계정/테이블 생성 (root 비밀번호 입력)
mysql -u root -p < sql/schema.sql

# 3) 환경설정
copy .env.example .env           # macOS/Linux: cp .env.example .env

# 4) 서버 실행
uvicorn app.main:app --reload

# 5) 다른 터미널에서 전체 시나리오 실행
python scripts/demo_client.py
```

Swagger UI: http://localhost:8000/docs
→ 브라우저가 쿠키를 저장하므로 `login` 실행 후 `me` 를 실행하면 그대로 인증됩니다.
(F12 → Application → Cookies 에서 쿠키 값 확인/수정 가능)

## 3. API 목록

| 구분 | 메서드 | 경로 | 설명 |
|---|---|---|---|
| 공통 | POST | `/users/signup` | 회원가입 (bcrypt 해시 저장) |
| 1-1 평문 쿠키 | POST | `/cookie/v1/login` | `user_id=1` 쿠키 발급 |
| | GET | `/cookie/v1/me` | 쿠키의 user_id로 사용자 조회 (**위조 가능**) |
| | POST | `/cookie/v1/logout` | 쿠키 삭제 |
| 1-2 서명 쿠키 | POST | `/cookie/v2/login` | `데이터.시각.서명` 형태 쿠키 발급 |
| | GET | `/cookie/v2/me` | 서명·만료 검증 후 사용자 조회 |
| | GET | `/cookie/v2/inspect` | 서명 쿠키 내용 디코딩 (암호화 아님을 확인) |
| | POST | `/cookie/v2/logout` | 쿠키 삭제 (서버 측 무효화는 불가) |
| 2 세션 | POST | `/session/login` | DB에 세션 저장, `session_id` 쿠키 발급 |
| | GET | `/session/me`, `/session/mypage` | 보호된 API (슬라이딩 만료 연장) |
| | GET | `/session/devices` | 내 로그인 기기 목록 |
| | POST | `/session/logout` | 현재 세션 DB 삭제 |
| | POST | `/session/logout-all` | 모든 기기 로그아웃 |

## 4. 수업 포인트: 세 방식 비교

| | 평문 쿠키 (v1) | 서명 쿠키 (v2) | 서버 세션 |
|---|---|---|---|
| 쿠키에 들어가는 값 | `user_id=1` | `{"uid":1}` + 서명 | 의미 없는 랜덤 ID |
| 상태 저장 위치 | 클라이언트 | 클라이언트 | **서버(DB)** |
| 위조 방지 | ❌ | ✅ (HMAC 서명) | ✅ (추측 불가 난수) |
| 내용 노출 | 노출 | **노출** (인코딩일 뿐) | 노출 안 됨 |
| 로그아웃 후 복사본 사용 | 가능 | **가능 (만료까지)** | 불가 (즉시 무효화) |
| 강제 로그아웃 / 기기 목록 | 불가 | 불가 | 가능 |
| 요청마다 DB 조회 | 사용자 조회 | 사용자 조회 | 세션 + 사용자 조회 |
| 서버 확장(여러 대) | 쉬움 | 쉬움 | 세션 저장소 공유 필요 (Redis 등) |

**JWT로 이어지는 연결고리**: 서명 쿠키(v2)는 JWT와 구조가 거의 같습니다
(`payload.signature`, 서버 저장소 없음, 내용은 Base64로 누구나 읽음).
따라서 v2에서 확인한 "로그아웃해도 토큰이 살아 있다"는 한계는 JWT에도 그대로 있고,
이를 보완하려고 Access Token을 짧게, Refresh Token을 서버에 저장하는 구조가 나옵니다.

## 5. 쿠키 보안 속성

| 속성 | 의미 | 이 코드의 설정 |
|---|---|---|
| `HttpOnly` | JS(`document.cookie`)에서 읽기 불가 → XSS로 쿠키 탈취 방지 | `True` |
| `Secure` | HTTPS에서만 전송 | `.env`의 `COOKIE_SECURE` (로컬은 False) |
| `SameSite=Lax` | 다른 사이트에서 오는 POST 등에 쿠키 미전송 → CSRF 완화 | `lax` |
| `Max-Age` | 쿠키 유효시간(초) | `SESSION_EXPIRE_MINUTES × 60` |

## 6. 실습 과제 예시

1. `curl -b "user_id=2" http://localhost:8000/cookie/v1/me` 로 평문 쿠키 위조를 직접 시연
2. `.env`의 `SECRET_KEY`를 바꾸고 서버를 재시작하면 기존 v2 쿠키가 어떻게 되는지 확인
3. 로그인 후 MySQL에서 `DELETE FROM login_sessions WHERE user_id=1;` 실행 → 관리자 강제 로그아웃 체험
4. `SESSION_EXPIRE_MINUTES=1` 로 바꾸고 만료/슬라이딩 연장 동작 관찰
5. (도전) 로그인 5회 실패 시 계정 잠금 기능 추가
6. (도전) 비밀번호 변경 API를 만들고, 변경 시 다른 기기 세션을 모두 삭제

## 참고
- `database.py`의 `echo=True` 로 바꾸면 실행되는 SQL이 콘솔에 출력되어 세션 조회 과정을 보여주기 좋습니다.
- 코드 안의 `Session`(SQLAlchemy DB 세션)과 로그인 세션(`LoginSession`)은 서로 다른 개념이니 수업 때 구분해 주세요.
