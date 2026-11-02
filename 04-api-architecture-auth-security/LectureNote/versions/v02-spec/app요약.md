이 앱은 **FastAPI와 MySQL로 만든 Todo REST API**이고, 강의 "API 아키텍처 & 인증 보안"의 2단계(v02-spec) 실습 버전입니다. 이 단계의 핵심은 **API 스펙(OpenAPI) 공개**입니다. 로그인 기능은 아직 없고, 모든 요청은 사용자 1번이 보낸 것으로 처리됩니다.

## 전체 요약

| 항목 | 내용 |
|---|---|
| 스택 | FastAPI, SQLAlchemy 2.0, PyMySQL(MySQL), Pydantic v2, python-dotenv |
| 버전 | `2.0.0`. 단계별 실습 v01~v04+ 중 2단계 |
| 단계 목표 | `/openapi.json`을 공개하고, 요청 모델(DTO) 검증과 API 명세가 함께 바뀌는지 확인. Postman으로 import해서 비교 |
| 구조 | 컨트롤러(Router) → 서비스(Service) → 저장소(Repository)의 3계층 |
| 인증 | 없음. [identity.py](app/identity.py)가 항상 `owner_id=1`을 돌려줌. JWT는 v03부터 |
| 문서 UI | Swagger(`/docs`)와 ReDoc은 꺼져 있고 `/openapi.json`만 켜져 있음 |

## 파일·기능별 요약

### 1. 앱 진입점과 공통 처리: [main.py](app/main.py)
- **시작할 때 DB 연결 확인**: 서버가 뜰 때 `SELECT 1`을 실행하고, 종료할 때 연결 풀을 정리합니다.
- **오류 응답 형식 통일**: 모든 오류를 `{"error": {"code": ...}}` 형태로 돌려줍니다.
  - HTTP 오류는 `detail` 값을 코드로 씁니다(예: `TODO_NOT_FOUND`).
  - 입력 검증 오류는 422와 `VALIDATION_ERROR`를 돌려주고, 필드별 위치·유형·메시지를 담습니다. 입력 원문은 넣지 않습니다.
  - 그 밖의 예외는 500과 `INTERNAL_ERROR`만 돌려주고, 내부 정보는 노출하지 않습니다.
- **보안 헤더**: 모든 응답에 `X-Content-Type-Options: nosniff`와 `Referrer-Policy: no-referrer`를 붙입니다. `/api/auth` 경로에는 `Cache-Control: no-store`도 붙입니다.
- **`GET /health`**: DB 연결을 확인하고 `{"status":"ok"}`를 돌려줍니다.

### 2. Todo API: [todos.py](app/todos.py)

| 메서드 | 경로 | 기능 | 성공 코드 |
|---|---|---|---|
| GET | `/api/todos` | 내 할 일 목록. `page`(1~1,000,000), `limit`(1~100, 기본 20), `completed` 필터. 최신순 | 200 |
| POST | `/api/todos` | 할 일 생성. 응답에 `Location` 헤더 포함 | 201 |
| GET | `/api/todos/{id}` | 상세 조회 | 200 |
| PATCH | `/api/todos/{id}` | 보낸 필드만 수정 | 200 |
| DELETE | `/api/todos/{id}` | 삭제 | 204 |

- **Repository**: 모든 조회 조건에 `owner_id`를 넣어서 남의 Todo에 접근하는 것(IDOR)을 막습니다. SQL은 파라미터 바인딩으로 실행합니다.
- **Service**: 트랜잭션(commit)을 관리합니다. Todo가 없을 때와 남의 Todo일 때 똑같이 404를 돌려줘서 존재 여부를 숨깁니다.
- **Router**: HTTP 계약을 담당합니다. 경로의 `id`는 1 이상 4294967295 이하로 제한합니다.

### 3. 입력·출력 모델: [schemas.py](app/schemas.py)
- `TodoCreate`: `title`은 앞뒤 공백을 지우고 1~200자여야 합니다. `completed`는 진짜 bool만 받습니다(엄격 모드). 정의되지 않은 필드는 거부합니다.
- `TodoPatch`: 빈 객체나 명시적인 `null`은 거부합니다. 최소 한 필드는 있어야 합니다.
- `TodoOut` / `TodoPage`: 응답 형식입니다. `owner_id`는 응답에 넣지 않습니다.

### 4. DB 모델: [models.py](app/models.py)
- 이번 단계에서 쓰는 테이블은 `users`와 `todos`입니다.
- `refresh_tokens`, `social_accounts`, `oauth_states`는 v03~v04(JWT, Google OAuth)를 위해 미리 정의만 해 둔 테이블입니다.
- 앱은 테이블을 만들지 않습니다(`create_all`을 호출하지 않음). 테이블 생성은 외부 SQL 스크립트로 합니다. 앱에 DDL 권한을 주지 않기 위해서입니다.

### 5. DB 연결: [database.py](app/database.py)
- `.env`에서 접속 정보를 읽습니다. 비밀번호에 특수문자가 있어도 안전하게 처리합니다.
- 연결할 때마다 시간대를 UTC로 고정하고, 끊긴 연결을 미리 확인하는 옵션(`pool_pre_ping`)과 연결 재활용 옵션(`pool_recycle`)을 켭니다.
- 요청마다 세션을 하나씩 만들고, 예외가 나면 롤백합니다.

**참고**: 사용자 인증이 없어서 누구나 1번 사용자의 데이터를 다룰 수 있습니다. 그래서 외부에 공개하면 안 되는 실습용 코드입니다(코드 주석에도 적혀 있습니다).
