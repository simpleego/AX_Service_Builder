# 4과목 · API 아키텍처 & 인증 보안 설계 (48H)

간단한 **개인 Todo API**를 REST 설계에서 인증·소셜 로그인·계층 분리·테스트까지 발전시키는 실습 자료입니다. 프런트엔드는 만들지 않고 Postman으로 요청과 응답을 확인합니다. 전체 과정의 2과목 FastAPI, 3과목 SQLAlchemy·RDB 모델링을 이어받도록 **Python 3.11 이상 + FastAPI + SQLAlchemy 2 + MySQL 8.0.16 이상**으로 작성했습니다.

## 구현 순서와 버전

각 폴더는 다른 버전의 소스를 import하지 않는 독립 실행 스냅샷입니다. 여기서 버전은 Git 태그가 아니라 **기능별 디렉터리**입니다. 인증 전에 API 계약과 DB를 먼저 준비하고, 로컬 인증을 익힌 다음 외부 로그인으로 확장합니다.

|순서|폴더|수업|새로 배우는 내용|확인할 산출물|
|---|---|---|---|---|
|1|[v01-rest](versions/v01-rest/README.md)|4-1 · 8H|리소스·URI·HTTP 메서드, CRUD, 상태코드, 페이지·필터|공용 계정 Todo CRUD|
|2|[v02-spec](versions/v02-spec/README.md)|4-2 · 6H|자연어 → 요청/응답 계약, 검증 규칙, OpenAPI|`/openapi.json`, 요구사항 추적표|
|3|[v03-jwt](versions/v03-jwt/README.md)|4-3 · 12H|회원가입·비밀번호 해시·JWT·소유권·refresh 회전·로그아웃|A/B 사용자 접근 차단|
|4|[v04-oauth](versions/v04-oauth/README.md)|4-4 · 8H|Google OAuth2 Authorization Code + PKCE + OIDC|Google 로그인 후 앱 JWT 발급|
|5|[v05-layered-swagger](versions/v05-layered-swagger/README.md)|4-5 · 8H|Controller/Service/Repository 분리·DI·트랜잭션·Swagger|`/docs`에서 명세와 호출 확인|
|6|[v06-postman](versions/v06-postman/README.md)|4-6 · 6H|환경변수·응답 스크립트·시나리오·부정 테스트|컬렉션 Runner와 통합 테스트|

합계 48시간. v02는 v01의 HTTP 동작을 유지하면서 계약과 명세 출력을 추가합니다. v05는 v04의 Todo 파일을 역할별로 분리하고 Swagger UI를 엽니다. v06은 v05 API 동작을 유지하며 별도 컬렉션과 자동 검증을 완성하는 단계입니다. 파일 비교로 구조 변경과 동작 변경을 구별하세요.

**추가 버전 [Idemcontents](versions/Idemcontents/README.md)**: v06 이후의 선택 심화 실습입니다. POST Idempotency-Key 중복 생성 방지·최초 응답 재생·키 충돌 409, 반복 PATCH의 UPDATE 생략, GET/DELETE 반복·롤백 검증을 포함합니다. DB 추가 SQL은 `database/03-idemcontents.sql`, 전용 컬렉션은 `postman/Idemcontents.postman_collection.json`입니다. [심화 실습 안내](docs/08-idemcontents.md)를 따르세요. 기존 48시간 기본안과 여섯 버전은 유지합니다.

## 가장 빠른 실행

1. [DB 준비](docs/02-database.md)에 따라 `database/00-admin.sql`과 `01-schema.sql`을 **관리자**로 실행합니다.
2. 처음 배우는 경우 v01, 전체 기능을 확인하려면 v06을 선택합니다.
3. 선택한 폴더에서 아래 명령을 실행합니다.

```powershell
cd versions/v06-postman
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env
# .env의 DB_PASSWORD를 수정한다.
python -c "import secrets; print(secrets.token_urlsafe(48))"
# 출력한 값을 .env의 JWT_SECRET에 넣는다. v03 이상에서 필수다.
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

`http://localhost:8000/health`가 `{"status":"ok"}`이면 DB까지 연결된 상태입니다. v05~v06의 Swagger는 `http://localhost:8000/docs`입니다. Google 설정을 비워도 일반 로그인·Todo는 실행되고, Google 시작 요청만 503을 반환합니다. 서버는 기본값인 로컬 주소에만 바인딩합니다.

4. Postman에 `postman/Todo-Course.postman_collection.json`, `postman/local.postman_environment.json`을 import하고 local 환경을 선택합니다.
5. v01~v02는 `01 Public CRUD` 폴더, v03 이상은 `02 Authenticated scenario` 폴더를 순서대로 실행합니다.

Google 로그인에는 브라우저와 실제 OAuth 클라이언트가 필요합니다. [소셜 로그인 안내](docs/04-auth-oauth.md)를 따르세요.

## 읽는 순서

- [48시간 강의 진행안과 전체 과정 연결](docs/01-teaching-plan.md)
- [MySQL 데이터베이스·테이블·계정 준비](docs/02-database.md)
- [자연어 요구사항과 API 계약](docs/03-api-contract.md)
- [JWT·리프레시 토큰·Google 소셜 로그인](docs/04-auth-oauth.md)
- [Postman 실행·시나리오·평가 기준](docs/05-postman.md)
- [계층형 아키텍처·버전별 변경 지도](docs/06-architecture.md)
- [검증 방법과 실제 검증 결과](docs/07-verification.md)

`scripts/build_course.py`는 버전 소스를 생성하는 관리용 스크립트입니다. 학생 실습에는 필요 없고, 재실행하면 버전 소스 수정이 덮어써집니다. `draft-nodejs/`는 기술 선택 전에 만든 보관 초안으로 수업·검증 대상이 아닙니다. **최종 자료는 루트의 versions/와 docs/, database/, postman/, tests/**입니다.

`output/todo-api-course.zip`은 보관 초안·가상환경·실제 .env를 제외한 최종 배포본입니다. 검증 당시 전체 Python 의존성은 requirements-lock.txt로 제공하며, 최신 허용 범위를 사용하려면 각 버전 requirements.txt를 설치하세요.

## 참고한 공식 문서

- [FastAPI JWT와 비밀번호 해시](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [SQLAlchemy 세션과 트랜잭션](https://docs.sqlalchemy.org/en/20/orm/session_basics.html)
- [Google OpenID Connect](https://developers.google.com/identity/openid-connect/openid-connect)
- [RFC 9700 OAuth 보안 권고](https://www.rfc-editor.org/rfc/rfc9700.html)

본 예제는 학습용 로컬 서버입니다. 운영 확장 항목(HTTPS, 로그인 요청 제한, 비밀번호 복구·이메일 검증, 토큰 보관 방식 등)은 인증 문서의 확장 과제로 구분했습니다.
