# React CDN 방식으로 한 파일에서 실행하기

CDN 방식은 **HTML 파일 하나에 React와 Babel(JSX 변환기)을 불러와서**, 설치나 빌드 없이 브라우저에서 바로 실행하는 방법입니다. 방법은 두 가지입니다.

---

## 방법 1. React 18 UMD 방식 (가장 간단, 수업용 추천)

`import` 없이 전역 변수 `React`, `ReactDOM`을 씁니다. 아래 내용을 `counter.html`로 저장하고 **더블클릭**하면 바로 실행됩니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>Counter - CDN</title>
  <!-- 1) React, ReactDOM -->
  <script crossorigin src="https://unpkg.com/react@18.3.1/umd/react.development.js"></script>
  <script crossorigin src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js"></script>
  <!-- 2) Babel: 브라우저에서 JSX를 일반 JavaScript로 바꿔 줍니다 -->
  <script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>

  <!-- 3) type="text/babel"이어야 JSX가 변환됩니다 -->
  <script type="text/babel">
    const { useState } = React; // import 대신 전역 React에서 꺼냅니다

    // 하위 컴포넌트
    function Counter() {
      const [count, setCount] = useState(0);

      return (
        <div>
          <p>현재 값: {count}</p>
          <button onClick={() => setCount(count + 1)}>+1</button>
          <button onClick={() => setCount(prev => prev - 1)}>-1</button>
        </div>
      );
    }

    // 상위 컴포넌트
    function App() {
      return (
        <div>
          <h1>카운터 예제</h1>
          <h2>첫 번째 카운터</h2>
          <Counter />
          <h2>두 번째 카운터</h2>
          <Counter />
        </div>
      );
    }

    // 화면에 붙이기 (main.jsx 역할)
    ReactDOM.createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

## 방법 2. React 19 + import map 방식 (최신 문법)

React 19부터는 UMD 파일이 없어서, **import map**으로 `import` 문을 그대로 씁니다. Vite 프로젝트 코드와 거의 같습니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <title>Counter - CDN (React 19)</title>
  <!-- 1) import 'react'가 어떤 주소를 가리킬지 정합니다 -->
  <script type="importmap">
    {
      "imports": {
        "react": "https://esm.sh/react@19.1.0",
        "react-dom/client": "https://esm.sh/react-dom@19.1.0/client"
      }
    }
  </script>
  <!-- 2) Babel -->
  <script src="https://unpkg.com/@babel/standalone@7.26.4/babel.min.js"></script>
</head>
<body>
  <div id="root"></div>

  <!-- 3) data-type="module"을 붙여야 import 문을 쓸 수 있습니다 -->
  <script type="text/babel" data-type="module">
    import { useState } from 'react';
    import { createRoot } from 'react-dom/client';

    function Counter() {
      const [count, setCount] = useState(0);
      return (
        <div>
          <p>현재 값: {count}</p>
          <button onClick={() => setCount(count + 1)}>+1</button>
          <button onClick={() => setCount(prev => prev - 1)}>-1</button>
        </div>
      );
    }

    function App() {
      return (
        <div>
          <h1>카운터 예제</h1>
          <Counter />
          <Counter />
        </div>
      );
    }

    createRoot(document.getElementById('root')).render(<App />);
  </script>
</body>
</html>
```

---

## 두 방법 비교

| 구분 | 방법 1 (UMD) | 방법 2 (import map) |
|---|---|---|
| React 버전 | 18 | 19 |
| Hook 가져오기 | `const { useState } = React;` | `import { useState } from 'react';` |
| 화면에 붙이기 | `ReactDOM.createRoot(...)` | `createRoot(...)` |
| script 태그 | `type="text/babel"` | `type="text/babel" data-type="module"` |
| 실행 | 더블클릭으로 열면 됨 | VS Code **Live Server**로 여는 것을 권장 |

## Vite 방식과 비교

| 구분 | CDN (HTML 한 파일) | Vite 프로젝트 |
|---|---|---|
| 설치 | 필요 없음 | Node.js, `npm install` 필요 |
| 파일 | `.html` 하나 | `main.jsx`, `App.jsx`, `Counter.jsx` 등 여러 개 |
| JSX 변환 | 브라우저에서 실행할 때 (느림) | 빌드할 때 미리 (빠름) |
| 용도 | 연습, 수업 예제, 간단한 데모 | 실제 프로젝트 |

## 주의할 점

- **인터넷 연결이 필요합니다.** CDN에서 React와 Babel을 내려받습니다.
- Babel이 브라우저에서 변환하므로 **실제 서비스용으로는 쓰지 않습니다.** 콘솔에 이와 관련된 경고가 뜨는 것은 정상입니다.
- 화면이 비어 있으면 F12 → Console 탭에서 오류를 확인하세요. `<script>` 태그의 `type="text/babel"`이 빠진 경우가 가장 흔합니다.
