# Todo Frontend (v01-rest)

v01 백엔드(FastAPI REST, 로그인 없음)에 맞춘 React + Vite 프론트엔드입니다.

## 기능
- 할 일 목록 (페이지당 10개, 이전/다음 페이지)
- 전체 / 진행 중 / 완료 필터 (`?completed=`)
- 추가 (`POST /api/todos`), 완료 토글·제목 수정 (`PATCH`), 삭제 (`DELETE`)
- 백엔드 연결 상태 표시 (`GET /health`)

## 실행
1. 백엔드 실행 (v01-rest 폴더):
   ```
   uvicorn app.main:app --reload --port 8000
   ```
2. 프론트엔드 실행 (이 폴더):
   ```
   npm install
   npm run dev
   ```
3. http://localhost:5173 접속

백엔드에 CORS 설정이 없어서 Vite 개발 서버가 `/api`, `/health` 요청을 `http://localhost:8000`으로 전달합니다.
백엔드 주소가 다르면 `VITE_API_TARGET` 환경변수로 바꿀 수 있습니다.
