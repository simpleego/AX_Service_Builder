# v04-oauth

4단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v04-oauth
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env
# .env의 DB_PASSWORD와 v03 이상 JWT_SECRET을 채운다.
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

macOS/Linux에서는 `.venv/bin/python`을 사용합니다. 반드시 이 버전 폴더에서 실행하세요.
다른 버전을 실행하기 전에 이전 서버를 Ctrl+C로 종료하세요.
v01~v02는 owner_id=1 고정이고, v03부터는 JWT 사용자만 자신의 Todo를 조회합니다.
v01에서 만든 Todo가 v03 신규 사용자에게 보이지 않는 것은 정상입니다.
DB는 한 번 준비하면 전 버전이 공유합니다. 버전 간 데이터 비교에는 다른 DB 이름을 사용할 수도 있습니다.

## 실습 목표 · OAuth2/OIDC (8H)
1. docs/04-auth-oauth.md에 따라 Google 웹 클라이언트와 redirect URI를 설정합니다.
2. oauth.py의 로그인 시작에서 state/nonce/verifier/binding의 차이를 확인합니다.
3. 브라우저로 로그인하고 callback의 앱 JWT를 Postman 환경에 복사합니다.
4. Postman 03 폴더로 소셜 사용자 Todo를 확인합니다.
5. 잘못된 state, 동의 취소, callback 재호출을 테스트합니다.
6. provider+sub로 식별하고 이메일로 자동 병합하지 않는 이유를 설명합니다.

완료 기준: Google 토큰과 앱 토큰의 역할을 구분하고 브라우저 로그인부터 Todo까지 연결합니다.
