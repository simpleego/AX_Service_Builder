// =============================================================
// vite.config.js — 개발 서버(Vite) 설정 파일
//
// Vite: React 코드를 브라우저가 이해하는 형태로 바꿔 주고,
//       코드를 저장하면 화면을 바로 새로고침해 주는 개발 도구.
// =============================================================

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react' // JSX 문법을 처리해 주는 플러그인

// 백엔드(FastAPI) 서버 주소. 환경변수 VITE_API_TARGET이 있으면 그 값을 쓴다.
const target = process.env.VITE_API_TARGET || 'http://localhost:8000'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // 프론트엔드 주소: http://localhost:5173

    // 프록시(proxy) = "대신 전달해 주는 중계자"
    //
    // 왜 필요할까?
    //   프론트(5173)와 백엔드(8000)는 포트가 달라서 브라우저가 "다른 사이트"로 본다.
    //   브라우저는 보안 규칙(CORS) 때문에 다른 사이트로 보내는 요청을 막는다.
    //   v01 백엔드에는 이를 허용하는 CORS 설정이 없다.
    //
    // 해결:
    //   브라우저는 같은 주소(5173)의 /api로 요청하고,
    //   Vite 개발 서버가 그 요청을 백엔드(8000)로 대신 보내 준다.
    //   예) localhost:5173/api/todos  →  localhost:8000/api/todos
    proxy: {
      '/api': { target, changeOrigin: true },
      '/health': { target, changeOrigin: true },
    },
  },
})
