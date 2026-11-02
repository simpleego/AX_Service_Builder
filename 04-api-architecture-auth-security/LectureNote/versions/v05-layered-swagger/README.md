# v05-layered-swagger

5단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v05-layered-swagger
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

## 실습 목표 · 계층/Swagger (8H)
1. v04의 todos.py와 v05의 세 파일을 나란히 비교합니다.
2. TodoRepository에는 SQL, TodoService에는 업무/commit, todos.py에는 HTTP 책임을 둡니다.
3. Depends(get_db), Depends(current_user)의 요청 흐름을 그립니다.
4. /docs에서 가입/로그인하고 Authorize 후 Todo CRUD를 호출합니다.
5. Postman 02 폴더를 다시 실행하여 구조 변경 뒤 동작이 같은지 확인합니다.

완료 기준: Controller→Service→Repository 호출 흐름과 트랜잭션 책임을 설명합니다.
