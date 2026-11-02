# v06-postman

6단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/v06-postman
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

## 실습 목표 · Postman 통합 검증 (6H)
1. Postman 컬렉션/환경을 import하고 토큰/ID 저장 스크립트를 확인합니다.
2. 02 폴더를 개별 Send 후 Runner로 순서 실행합니다.
3. A/B 소유권, 잘못된 입력, refresh 재사용/로그아웃을 검증합니다.
4. docs/05-postman.md의 추가 수동 테스트를 수행합니다.
5. 루트 tests/로 자동 검증하고 대체 DB와 MySQL 검증의 차이를 기록합니다.

완료 기준: 성공/실패 시나리오와 예상 상태코드를 포함한 재현 가능한 검증 결과를 제출합니다.
