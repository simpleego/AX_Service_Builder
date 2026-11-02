# v02-spec

2단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v02-spec
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

## 실습 목표 · API 스펙 (6H)
1. docs/03-api-contract.md의 R01~R04를 자연어에서 요청/응답 표로 변환합니다.
2. v01 main.py와 비교하여 openapi_url 활성화를 확인합니다.
3. GET /openapi.json으로 paths와 components.schemas를 읽습니다.
4. title 최대 길이를 변경하면 DTO 검증과 명세가 함께 바뀌는지 확인합니다.
5. Postman에서 OpenAPI import를 해보고 제공 컬렉션과 상태코드를 비교합니다.

완료 기준: 입력/출력/필수값/상태코드/오류를 다른 팀이 구현할 수 있게 설명합니다.
