# v02-spec

2단계 독립 실행 스냅샷. 공통 실행/DB 준비는 루트 README.md와 docs/02-database.md를 먼저 읽으세요.

```powershell
cd versions/v02-spec
npm install
Copy-Item .env.example .env
# .env의 DB 비밀번호와 v03 이상 JWT_SECRET을 설정
npm start
```

이전 서버를 Ctrl+C로 종료하고 다음 버전을 실행하세요. 포트는 공통으로 3000입니다.
v01~v02는 owner_id=1 고정, v03부터는 회원가입한 사용자의 JWT로만 접근합니다.
v01~v02에서 만든 데이터가 v03 신규 사용자에게 보이지 않는 것은 소유권 분리의 정상 결과입니다.
공통 DB 스키마는 모든 버전을 지원합니다. DB 초기화는 한 번만 수행하세요.
