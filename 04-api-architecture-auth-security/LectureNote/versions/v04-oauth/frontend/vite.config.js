import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// 개발 서버에서 /api 요청을 FastAPI(8000)로 넘긴다.
// 브라우저 입장에서는 같은 출처(localhost:5180)라서 백엔드에 CORS 설정이 필요 없다.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5180,
    strictPort: true, // 백엔드 FRONTEND_URL과 포트가 같아야 Google 로그인 후 돌아올 수 있다.
    proxy: {
      '/api': { target: 'http://127.0.0.1:8000' },
      '/health': { target: 'http://127.0.0.1:8000' },
    },
  },
});
