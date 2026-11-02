# Idemcontents · 멱등성 추가 실습

v06-postman을 기반으로 한 일곱 번째 독립 실행 버전입니다. 기존 JWT·Google 로그인·Swagger를 포함합니다.
먼저 공통 DB 준비 후 **database/03-idemcontents.sql**을 관리자 계정으로 추가 실행합니다.

```sql
SOURCE D:/AX_FullStack_Builder/04-api-architecture-auth-security/LectureNote/database/03-idemcontents.sql;
```

```powershell
cd versions/Idemcontents
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env
# .env의 DB_PASSWORD와 v03 이상 JWT_SECRET을 채운다.
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

macOS/Linux에서는 `.venv/bin/python`을 사용합니다. 반드시 이 버전 폴더에서 실행하세요.
다른 버전을 실행하기 전에 이전 서버를 Ctrl+C로 종료하세요.
DB에는 기존 테이블을 유지하면서 idempotency_records 테이블만 추가합니다. Google 설정은 선택입니다.

## 실습 목표 · 멱등성 (추가 4~6H)

1. 키 없는 POST를 두 번 보내 서로 다른 ID를 확인합니다.
2. 같은 Idempotency-Key와 본문으로 두 번 보내 한 번만 생성되는지 확인합니다.
3. 같은 키에 다른 본문을 보내 409를 확인합니다.
4. 반복 GET·PATCH·DELETE와 SQL 쓰기 생략, 롤백 테스트를 수행합니다.
5. 별도 MySQL 테스트 DB가 있으면 동시성 테스트를 수행합니다.

|요청|동작|
|---|---|
|POST, 키 없음|매번 생성|
|POST, 같은 사용자·키·본문|최초 201·본문·Location 재생|
|POST, 같은 사용자·키·다른 본문|409 IDEMPOTENCY_KEY_CONFLICT|
|POST, 같은 키·다른 사용자|각자 독립적으로 생성|
|PATCH 같은 값|UPDATE SQL 생략, updated_at 유지|
|GET 반복|조회만 수행|
|DELETE 반복|처음 204, 이후 404, 삭제 상태 유지|

```http
POST /api/todos
Authorization: Bearer <accessToken>
Content-Type: application/json
Idempotency-Key: todo-request-001

{"title":"멱등성 실습","completed":false}
```

최초 `Idempotency-Replayed: false`, 재생 `true`. 키는 영문/숫자/`._:-` 1~128자이며 잘못된 형식은 400입니다. 헤더가 없으면 재생 표시도 생략합니다. 이 헤더 형식과 충돌 409는 이 예제의 앱 계약이며 표준 초안 전체 구현을 주장하지 않습니다.

## 구현과 검증

- app/idempotency.py: 키·본문 해시, 사용자 행 잠금, 최초 응답 기록, 원자적 커밋.
- app/models.py: 사용자·작업·키 UNIQUE ORM 매핑.
- app/todos.py: 선택 헤더와 재생 응답.
- app/todo_service.py: 같은 값 PATCH의 명시적인 no-op 처리.
- tests/test_idempotency.py: HTTP/DB 행 수/쓰기 SQL/실패 롤백 테스트.
- tests/test_idempotency_mysql.py: 실제 MySQL 동시 요청 선택 테스트.

Postman에 루트의 `postman/Idemcontents.postman_collection.json`과 기존 `local.postman_environment.json`을 import하고 Todo local 환경에서 전용 컬렉션을 순서대로 실행합니다. 첫 요청이 새 사용자와 키를 준비합니다.

루트 폴더에서:

```powershell
.venv/Scripts/python -m pip install -r requirements-dev.txt
$env:TEST_VERSION='Idemcontents'
.venv/Scripts/python -m pytest -q tests
Remove-Item Env:TEST_VERSION
```

## 보장 범위

키 범위는 인증 사용자 + POST:/api/todos + 키입니다. 검증된 DTO를 정규화하므로 JSON 필드 순서, 제목 앞뒤 공백, completed 기본값 생략은 같은 요청입니다. 성공한 201만 보관하고 입력/인증 오류·롤백된 요청은 키를 점유하지 않습니다.

Todo와 응답 기록은 한 트랜잭션에 저장됩니다. 사용자 행 잠금으로 같은 사용자의 키 있는 POST를 직렬화하며 여러 worker에서도 DB 잠금이 적용됩니다. 수업용 단순 구현으로, 키별 예약 방식보다 병렬성은 낮습니다. 잠금 시간 초과 등 일시적 실패는 같은 키·본문으로 재시도합니다.

기록에 TTL은 없습니다. Todo를 수정·삭제해도 최초 응답을 재생하며 삭제한 Todo를 다시 만들지 않습니다. 최초 응답은 현재 리소스 상태가 아닙니다. 기록을 지우면 과거 요청의 중복 방지 보장이 끝납니다. 운영에는 용량과 개인정보 보관·재시도 허용 기간 정책이 필요합니다.

기존 SQLAlchemy도 실질 변경이 없으면 UPDATE를 생략할 수 있습니다. 이번 버전은 명시적 비교와 쓰기 SQL 테스트로 의도를 드러냅니다. 수정 시각 보존은 추가 계약이며 HTTP 멱등성의 필수 요건 자체는 아닙니다.

다른 요청이 중간에 데이터를 변경하는 상황까지 PATCH/DELETE 응답을 고정하는 기능, PUT, 인증 API의 멱등 키는 포함하지 않습니다. 자세한 흐름과 MySQL 검증은 ../../docs/08-idemcontents.md를 보세요.

완료 기준: 중복 생성 방지·키 충돌·반복 요청·트랜잭션 원자성을 재현하고 정책을 설명합니다.
