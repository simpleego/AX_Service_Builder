# v01-rest

1단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v01-rest
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

## 실습 목표 · REST (8H)
1. database.py의 get_db와 models.py의 User/Todo 관계를 읽고 /health를 호출합니다.
2. schemas.py에서 제목/완료 여부의 제약을 확인합니다.
3. todos.py에서 POST → GET 목록 → 상세 → PATCH → DELETE 순서로 구현을 따라갑니다.
4. Postman 01 폴더를 실행하고 201의 Location과 204의 빈 본문을 확인합니다.
5. page/limit/completed 쿼리를 바꾸고 빈 제목/잘못된 ID를 테스트합니다.

완료 기준: CRUD 5개 경로가 동작하고 소스의 owner_id=1 고정이 학습용임을 설명할 수 있습니다.
