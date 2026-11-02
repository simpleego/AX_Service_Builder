# 자연어 요구사항 → API 계약

## 요구사항 추적표

|ID|자연어 요구사항|API/검증 규칙|버전|
|---|---|---|---|
|R01|할 일을 등록한다|POST /api/todos, title 1~200자, 201+Location|v01|
|R02|목록을 페이지로 보고 완료 여부로 검색한다|GET /api/todos?page=1&limit=20&completed=false|v01|
|R03|할 일을 수정하고 삭제한다|PATCH /api/todos/{id}, DELETE /api/todos/{id}|v01|
|R04|요청/응답을 개발 전에 합의한다|DTO와 상태코드, /openapi.json 자동 생성|v02|
|R05|가입한 사용자만 자신의 할 일을 관리한다|register/login, Bearer JWT, owner_id SQL 조건|v03|
|R06|로그인 상태를 안전하게 연장하고 종료한다|refresh 회전/재사용 family 폐기/logout|v03|
|R07|Google 계정으로 로그인한다|Google code+PKCE, OIDC ID 토큰 검증, 앱 JWT|v04|
|R08|문서를 쉽게 보고 구조를 유지보수한다|Controller→Service→Repository, /docs|v05|
|R09|정상·실패 시나리오를 반복 검증한다|Postman 컬렉션과 환경, pytest|v06|

## REST 설계 원칙을 적용하는 방법

URI는 명사 복수형 `/api/todos`, 개별 리소스는 `/api/todos/123`으로 표현합니다. `/createTodo`, `/deleteTodo`처럼 동작을 URI에 넣지 않습니다. 동작은 HTTP 메서드로 표현합니다. 인증은 리소스 CRUD와 성격이 달라 `/api/auth/login` 등의 작업 엔드포인트로 분리합니다.

GET은 조회이며 서버 상태를 바꾸지 않습니다. POST는 생성이므로 재전송하면 중복 생성될 수 있습니다. PATCH는 전달 필드만 변경하며 이 예제의 단순 필드 대입은 같은 값으로 반복 호출해도 결과가 같습니다. DELETE는 처음 204, 재호출은 404이지만 삭제된 서버 상태는 같습니다. PUT 전체 교체는 구현 범위에 넣지 않았습니다. CORS 설정은 브라우저 프런트 연결 시 추가하며 Postman에는 필요하지 않습니다. 이 예제는 리소스 중심 HTTP API로, HATEOAS까지 구현한 완전한 REST 성숙도 모델을 목표로 하지 않습니다.

## Todo API

v01~v02는 공용 사용자 1번으로 실행합니다. v03 이상은 모든 Todo 요청에 `Authorization: Bearer <accessToken>`이 필요합니다. owner_id는 클라이언트가 입력할 수 없으며 서버가 JWT sub에서 결정합니다.

|메서드|경로|요청|성공|대표 실패|
|---|---|---|---|---|
|GET|/health|없음|200 DB 연결 확인|500 DB 오류|
|POST|/api/todos|title, completed 선택|201 Todo + Location|422 입력 오류|
|GET|/api/todos|page/limit/completed 선택|200 목록 envelope|422 범위/형식 오류|
|GET|/api/todos/{id}|양의 정수 ID|200 Todo|404 없음/타인, 422 잘못된 ID|
|PATCH|/api/todos/{id}|title/completed 중 하나 이상|200 Todo|404, 422 빈 객체/null/잘못된 타입|
|DELETE|/api/todos/{id}|없음|204 빈 본문|404, 422|

v03 이상 Todo API 공통 오류는 401 인증 실패입니다. 제목은 앞뒤 공백 제거 후 1~200자, completed는 JSON boolean만 허용합니다. 추가 필드, owner_id 입력, 빈 PATCH, null 값은 422입니다. JSON 문법 오류도 FastAPI 검증 오류인 422로 반환합니다. 400은 OAuth state 등 의미상 잘못된 요청에 사용합니다. page는 1~1,000,000, limit는 1~100입니다. 정렬은 id 내림차순이고 응답에 total은 포함하지 않습니다.

```http
POST /api/todos
Content-Type: application/json
Authorization: Bearer <accessToken>

{"title":"REST 설계 복습","completed":false}
```

```json
{"id":12,"title":"REST 설계 복습","completed":false,"created_at":"2026-10-31T01:00:00","updated_at":"2026-10-31T01:00:00"}
```

created_at/updated_at는 DB UTC 시간이며 현재 예제의 JSON은 시간대 접미사 없는 ISO datetime으로 직렬화합니다. 후속 프런트 구현에서는 UTC로 해석하거나 출력 DTO에서 `Z`를 붙이는 정책을 합의하세요.

```json
{"data":[{"id":12,"title":"REST 설계 복습","completed":false,"created_at":"2026-10-31T01:00:00","updated_at":"2026-10-31T01:00:00"}],"page":1,"limit":20}
```

## 인증 API (v03 이상)

|메서드|경로|본문|성공|실패|
|---|---|---|---|---|
|POST|/api/auth/register|email, password|201 id/email|409 중복, 422 형식|
|POST|/api/auth/login|email, password|200 TokenPair|401 실패, 422 형식|
|POST|/api/auth/refresh|refreshToken|200 새 TokenPair|401 만료/재사용/미등록, 422 형식|
|POST|/api/auth/logout|refreshToken|204|422 형식|
|GET|/api/auth/google|브라우저 요청|302 Google 이동|503 미설정|
|GET|/api/auth/google/callback|code/state + 쿠키|200 앱 TokenPair|400 state/취소, 401 검증 실패|

Google 두 경로는 v04부터 존재합니다. logout은 알려지지 않은 올바른 형식의 토큰에도 204를 반환하는 멱등 동작입니다. 로컬 로그인은 JSON 기반 앱 자체 인증입니다. OAuth2 Password Grant를 구현한 것으로 부르지 않습니다. Google 로그인의 OAuth2 Authorization Code 흐름과 구별하세요.

```json
{"accessToken":"eyJ...","refreshToken":"43-character-opaque-random-token-value-here___","tokenType":"Bearer","expiresIn":900}
```

위 토큰 문자열은 구조 설명용이며 실제 요청에는 로그인 응답을 사용합니다. 비밀번호 길이는 12~128자이고 이메일은 소문자로 정규화합니다. 응답에는 비밀번호 해시를 포함하지 않습니다.

## 오류 공통 형식

```json
{"error":{"code":"TODO_NOT_FOUND"}}
```

422에는 `fields` 배열(loc/type/message)이 추가되고 입력 원문은 포함되지 않습니다. 내부 예외는 500 `INTERNAL_ERROR`로 숨깁니다. 일반적인 없는 경로의 code는 Starlette 기본 상세 문자열일 수 있습니다.

v02부터 `/openapi.json`을 Postman에서 읽거나 import할 수 있습니다. v05부터 `/docs`에서 Swagger UI가 같은 명세를 렌더링합니다. 자동 생성 항목은 경로·입출력 DTO·필수값·제약·Bearer 보안 스키마이고, 트랜잭션/재사용 탐지 정책은 이 문서로 보완합니다. 동작 변경 시 DTO와 문서를 함께 바꾸어 명세가 어긋나지 않도록 합니다.
