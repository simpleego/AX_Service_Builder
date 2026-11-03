// =============================================================
// main.jsx — 앱의 시작점(entry point)
// index.html이 이 파일을 불러오고, 이 파일이 React 앱을 화면에 그린다.
// =============================================================

// StrictMode: 개발 중에 잠재적인 실수를 찾아 경고해 주는 React 도구.
//   (개발 모드에서만 동작하고, 실제 배포 화면에는 영향이 없다.)
import { StrictMode } from 'react'
// createRoot: React가 그림을 그릴 "도화지"를 만드는 함수.
import { createRoot } from 'react-dom/client'
// App: 우리가 만든 최상위 화면 컴포넌트.
import App from './App.jsx'
// 전체 화면에 적용할 CSS(디자인) 파일.
import './index.css'

// index.html 안의 <div id="root"></div>를 찾아 그 안에 <App />을 그린다.
createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
