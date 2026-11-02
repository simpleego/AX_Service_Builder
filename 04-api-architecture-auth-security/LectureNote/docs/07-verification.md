# 검증 결과와 재실행 방법

## 추가 버전 Idemcontents 검증

Idemcontents는 기존 32개 회귀 항목에 멱등성 검증 9개를 더하여 **41개 통과, 실제 MySQL 동시성 1개 제외**입니다. 같은 사용자·키 응답 재생, 다른 본문 충돌, 사용자/키 범위, 키 없는 중복 생성, 잘못된 키/입력, 기록 실패의 원자적 롤백, GET/PATCH의 쓰기 SQL 미발행, DELETE 반복을 확인했습니다. 자동 검증은 SQLite 대체 DB이며 MySQL 동시성 테스트는 별도 DB URL 미설정으로 실행하지 않았습니다. 전용 Postman 18개 요청은 문법 검사를 수행하며 실제 Runner 실행 결과와 구별합니다. 자세한 실행법은 docs/08-idemcontents.md를 따릅니다.

## 검증 환경과 결과 (2026-10-31)

Python 3.12 / Windows에서 requirements-lock.txt의 의존성을 설치했습니다. `python scripts/check.py`로 최종 Python/JSON 파일 문법 및 여섯 버전의 필수 파일을 검사했습니다. 실제 FastAPI 앱에서 v02~v06 OpenAPI 문서를 생성해 specs/에 저장했습니다.

|버전|통과|의도적 제외|대상|
|---|---:|---:|---|
|v01 REST|18|14|CRUD/검증/health, 인증 기능 미도입|
|v02 Spec|18|14|CRUD/검증/명세, 인증 기능 미도입|
|v03 JWT|29|3|CRUD/JWT/소유권/refresh, Google 미도입|
|v04 OAuth|32|0|전체 API + Google mock|
|v05 Layered|32|0|계층 분리 이후 회귀 검증|
|v06 Postman|32|0|최종 API 회귀 검증|

각 버전은 새 프로세스로 import하여 다른 버전의 패키지 캐시가 결과를 오염시키지 않도록 했습니다. SQLite 대체 DB를 사용하는 테스트 합계는 161개 통과이며, 단계에 아직 없는 기능은 제외합니다. 테스트 대상은 HTTP CRUD 계약, 입력 오류, 소유권, 비밀번호/refresh 저장, JWT 변조·만료·issuer/audience/type/필수 claim, refresh 회전/재사용/로그아웃, OAuth state/브라우저 쿠키/nonce/신원 연결입니다.

설치된 Starlette에서 httpx 기반 TestClient의 향후 변경에 대한 deprecation warning이 한 번씩 발생합니다. 현재 테스트 실패는 아니며, 테스트 도구를 갱신할 때 httpx2 전환을 검토하세요. 실행 의존성과 당시 테스트 도구의 정확한 버전은 requirements-lock.txt에 보관했습니다.

## 검증 범위의 한계

이 환경에는 localhost:3306에서 실행 중인 MySQL이 없고 Docker 엔진도 실행 중이지 않았습니다. 따라서 **실제 MySQL DDL 적용, 행 잠금의 동시성, MySQL 사용자 권한, 인덱스 실행계획, 실제 Postman/Newman Runner 실행은 여기서 완료하지 않았습니다.** SQLite 테스트 통과를 MySQL 통합 검증으로 간주하지 않습니다.

Google 응답과 ID 토큰 검증 함수는 자동 테스트에서 mock합니다. 실제 Google 클라이언트 등록·동의 화면·ID Token 서명 검증·네트워크 교환은 사용자 환경의 실 계정으로 확인해야 합니다. 실제 토큰/자격증명은 생성하거나 저장하지 않았습니다.

## 재실행

루트 폴더에서 실행합니다.

```powershell
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements-dev.txt
# 검증 당시 전체 버전을 재현하려면 대신: pip install -r requirements-lock.txt
.venv/Scripts/python scripts/check.py
.venv/Scripts/python scripts/test_all_versions.py
.venv/Scripts/python scripts/export_openapi.py v06-postman
```

특정 버전만 검사할 경우:

```powershell
$env:TEST_VERSION='v03-jwt'
.venv/Scripts/python -m pytest -q tests
Remove-Item Env:TEST_VERSION
```

테스트는 별도 대체 DB를 쓰므로 실제 todo_course 데이터를 변경하지 않습니다. Windows 제한 환경에서 asyncio 내부 소켓 생성이 멈추면 일반 로컬 터미널에서 실행하세요.

## MySQL 현장 검증 순서

1. database/00-admin.sql, 01-schema.sql을 적용하고 SHOW CREATE TABLE로 제약/인덱스를 확인합니다.
2. v01 서버에서 Postman 01 폴더를 실행합니다.
3. v03 서버에서 Postman 02 폴더를 실행하고 DB refresh 행 폐기를 확인합니다.
4. 같은 refresh token으로 거의 동시에 두 요청을 전송하여 하나만 회전에 성공하고 family가 폐기되는지 확인합니다. 로그/응답에 토큰 원문을 남기지 않습니다.
5. v04에서 실제 Google 로그인 후 03 폴더를 실행합니다.
6. v05/v06에서 02 폴더를 재실행하고 Swagger 명세와 상태코드를 비교합니다.

수업 시작 전 강사가 이 현장 검증을 한 번 수행하면 DB 접속 정보와 Google 콘솔 설정으로 인한 수업 지연을 줄일 수 있습니다.
