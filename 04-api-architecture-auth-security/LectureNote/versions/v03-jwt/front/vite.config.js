import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// /api 요청을 FastAPI 서버(8000)로 전달한다.
// 브라우저 입장에서는 같은 출처(5173)라서 백엔드에 CORS 설정을 추가하지 않아도 된다.
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
