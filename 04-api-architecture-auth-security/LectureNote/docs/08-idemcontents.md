# Idemcontents 추가 버전 · 멱등성 실습

v06 이후의 독립 심화 버전입니다. 실행/요청 예시는 [버전 README](../versions/Idemcontents/README.md)를 참고하세요. 기존 여섯 버전 서버 동작은 변경하지 않았습니다.

## 진행 순서 (추가 4~6시간)

1. GET/DELETE의 HTTP 멱등성과 POST에 앱이 제공하는 중복 방지 계약을 구별합니다.
2. database/03-idemcontents.sql을 적용하고 키 범위와 UNIQUE 제약을 확인합니다.
3. 가입/로그인 후 키 없는 POST를 두 번 보내 서로 다른 ID를 확인합니다.
4. 키 있는 POST를 반복해 같은 ID·본문·Location·201과 재생 표시를 확인합니다.
5. 같은 키의 본문 변경은 409, 새 키는 새 생성이 되는지 확인합니다.
6. 반복 PATCH의 updated_at 유지와 UPDATE SQL 미발행 테스트를 읽습니다.
7. GET 반복 전후 불변, DELETE의 204→404와 삭제 상태 유지를 확인합니다.
8. 기록 저장 실패 시 Todo도 롤백되는지 테스트합니다.
9. 별도 MySQL DB가 있다면 동시성 테스트를 실행합니다.

## 저장과 재생 흐름

```mermaid
flowchart TD
    A[인증·DTO·키 형식 검증] --> B[사용자 행 FOR UPDATE 잠금]
    B --> C{사용자·작업·키 기록 존재?}
    C -->|아니오| D[Todo 생성 flush]
    D --> E[최초 응답 기록]
    E --> F[한 번에 commit]
    C -->|예| G{본문 해시 일치?}
    G -->|예| H[최초 응답 재생]
    G -->|아니오| I[409 충돌]
```

DB 기록은 서버 재시작·다른 worker에서도 유지됩니다. commit 후 응답 전달 실패에도 재요청으로 중복 생성되지 않습니다. commit 전 실패는 Todo와 기록이 함께 rollback됩니다. 사용자 행 잠금, 최신 기록을 읽는 FOR UPDATE, UNIQUE 제약을 함께 사용합니다.

## MySQL 동시성 선택 테스트

기본 테스트는 SQLite 대체 DB이므로 HTTP/저장/SQL 발행을 검사하지만 **MySQL 행 잠금 검증은 아닙니다**. 테스트 전용 MySQL DB에 01-schema.sql과 03-idemcontents.sql의 구조를 준비하세요. SQL의 USE todo_course는 테스트 DB명으로 바꾼 별도 스크립트를 사용합니다. 계정에는 해당 DB의 DML 권한이 필요합니다.

```powershell
$env:TEST_VERSION='Idemcontents'
# 실제 비밀번호를 안전하게 설정합니다. URL 특수문자는 인코딩이 필요합니다.
$env:IDEMPOTENCY_MYSQL_TEST_URL='mysql+pymysql://test_user:password@localhost:3306/todo_course_test?charset=utf8mb4'
.venv/Scripts/python -m pytest -q tests/test_idempotency_mysql.py
Remove-Item Env:IDEMPOTENCY_MYSQL_TEST_URL
Remove-Item Env:TEST_VERSION
```

4개 독립 세션이 같은 사용자·키로 동시 요청하며 최초 생성 1건/재생 3건과 Todo/기록 각 1행을 검사합니다. 테스트가 만든 사용자와 종속 데이터만 정리합니다. URL 미설정 시 의도적으로 제외됩니다. 운영 DB는 사용하지 마세요.

## 정책 확인

- 헤더가 없는 POST는 매번 생성합니다. 같은 키라도 사용자가 다르면 독립적입니다.
- 인증/DTO 검증을 재생 전에 수행하므로 만료 JWT로 과거 응답을 받지 못합니다.
- 최초 응답 스냅샷은 현재 리소스 상태가 아닙니다. 삭제 후 재시도도 재생만 하고 재생성하지 않습니다.
- 기록은 TTL 없이 보관합니다. 지우면 과거 중복 방지 보장이 끝납니다. 토큰은 기록하지 않지만 Todo 제목은 스냅샷에 남습니다.
- 오류 응답은 저장하지 않습니다. 일시적 실패는 같은 키와 본문으로 재시도합니다.
- HTTP 멱등성은 응답 코드가 같다는 뜻이 아닙니다. DELETE 204→404는 멱등입니다.
- 수정 시각 보존은 이 앱의 추가 계약입니다. HTTP 멱등성이 부수적인 로그/이력의 완전한 불변까지 요구하지는 않습니다.

근거: [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2), [SQLAlchemy Session.is_modified](https://docs.sqlalchemy.org/en/20/orm/session_api.html#sqlalchemy.orm.Session.is_modified).
