# v03-jwt

3단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v03-jwt
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

## 실습 목표 · JWT (12H)
1. security.py의 scrypt 해시와 password_matches를 먼저 읽습니다.
2. auth.py에서 register/login을 구현하고 DB에 평문이 없는지 확인합니다.
3. identity.py가 JWT current_user를 사용하도록 바뀐 점을 비교합니다.
4. A/B 사용자를 만들고 같은 Todo ID로 조회/수정/삭제해 소유권을 확인합니다.
5. refresh 정상 회전 → 이전 토큰 재사용 → 새 토큰 거부를 순서대로 관찰합니다.
6. logout 이후 refresh와 access의 유효성이 다른 이유를 설명합니다.

완료 기준: Postman 02 폴더 통과와 비밀/원문 토큰을 DB·로그에 남기지 않는 설계를 설명합니다.
