React에서 Tailwind CSS를 사용하는 아주 간단한 예제 5개를 작성하겠습니다. 입문자가 이해하기 쉽도록 각각 다른 Tailwind 기능을 사용하고, React의 기본 기능도 함께 익힐 수 있도록 구성했습니다.

## 1. 프로젝트 환경 설정

React + Vite + Tailwind CSS v4 기준입니다.

```
# React 프로젝트 생성
npm create vite@latest tailwind-react -- --template react

cd tailwind-react

# 패키지 설치
npm install

# Tailwind CSS 설치
npm install tailwindcss @tailwindcss/vite
```

`vite.config.js`

```
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

`src/index.css`

```
@import "tailwindcss";
```

`src/main.jsx`에서 `./index.css`를 import하면 됩니다.

## 예제 1. 텍스트와 배경색 적용

## 안녕하세요 React!

Tailwind CSS 첫 번째 예제

```
function App() {
  return (
    <div className="bg-blue-100 p-6">
      <h1 className="text-2xl font-bold text-blue-700">
        안녕하세요 React!
      </h1>
      <p className="text-gray-700">
        Tailwind CSS 첫 번째 예제
      </p>
    </div>
  );
}

export default App;
```

| 클래스             | 의미         |
| --------------- | ---------- |
| `bg-blue-100`   | 연한 파란색 배경  |
| `p-6`           | 안쪽 여백 24px |
| `text-2xl`      | 글자 크기 24px |
| `font-bold`     | 굵은 글씨      |
| `text-blue-700` | 진한 파란색 글씨  |

## 예제 2. 버튼 스타일과 Hover 효과

저장하기버튼에 마우스를 올리면 색상이 진해집니다.

```
function App() {
  return (
    <button
      className="bg-blue-500 hover:bg-blue-700
                 text-white px-6 py-3 rounded-lg"
    >
      저장하기
    </button>
  );
}

export default App;
```

| 클래스                 | 의미              |
| ------------------- | --------------- |
| `bg-blue-500`       | 기본 파란색          |
| `hover:bg-blue-700` | 마우스를 올리면 진한 파란색 |
| `text-white`        | 흰색 글씨           |
| `px-6`              | 좌우 여백 24px      |
| `py-3`              | 상하 여백 12px      |
| `rounded-lg`        | 둥근 모서리          |

## 예제 3. 상품 카드 만들기

## 노트북

고성능 업무용 노트북

### 1,200,000원

구매하기

```
function App() {
  return (
    <div className="w-64 p-6 bg-white rounded-xl shadow-md">
      <h2 className="text-xl font-bold">
        노트북
      </h2>

      <p className="text-gray-500 mt-2">
        고성능 업무용 노트북
      </p>

      <p className="text-lg font-bold mt-3">
        1,200,000원
      </p>

      <button className="bg-green-600 text-white
                         px-4 py-2 rounded mt-3">
        구매하기
      </button>
    </div>
  );
}

export default App;
```

새로운 클래스는 `w-64`(너비 256px), `shadow-md`(그림자), `mt-3`(위쪽 여백 12px)입니다.

## 예제 4. Flexbox를 이용한 가로 배치

메뉴 1

메뉴 2

메뉴 3

```
function App() {
  return (
    <div className="flex gap-4 p-4">
      <div className="bg-red-500 text-white p-4">
        메뉴 1
      </div>

      <div className="bg-green-500 text-white p-4">
        메뉴 2
      </div>

      <div className="bg-blue-500 text-white p-4">
        메뉴 3
      </div>
    </div>
  );
}

export default App;
```

핵심 클래스는 `flex`(가로 배치), `gap-4`(요소 사이 간격 16px)입니다.

## 예제 5. React State와 Tailwind를 이용한 색상 변경

이번 예제는 React의 `useState`를 사용하여 버튼 클릭 시 배경색이 변경되도록 구현합니다.

비활성화 상태

상태 변경

```
import { useState } from "react";

function App() {
  const [active, setActive] = useState(false);

  return (
    <div className="p-6">

      <div className={`p-6 text-white rounded-lg
        ${active ? "bg-green-500" : "bg-red-500"}`}
      >
        {active ? "활성화 상태" : "비활성화 상태"}
      </div>

      <button
        onClick={() => setActive(!active)}
        className="bg-blue-500 text-white
                   px-4 py-2 rounded mt-4"
      >
        상태 변경
      </button>

    </div>
  );
}

export default App;
```

여기서 중요한 부분은 다음 코드입니다.

```
className={active ? "bg-green-500" : "bg-red-500"}
```

React의 상태에 따라 서로 다른 Tailwind 클래스를 적용하는 것입니다. 클래스 이름을 완전한 문자열로 작성했기 때문에 Tailwind가 두 클래스를 모두 찾아서 CSS를 생성할 수 있습니다.

## 5개 예제 핵심 정리

| 예제 | Tailwind 핵심 기능 | React 핵심 기능 |
| -- | -------------- | ----------- |
| 1  | 글자 크기, 색상, 여백  | JSX         |
| 2  | 버튼, Hover 효과   | JSX 속성      |
| 3  | 카드, 테두리, 그림자   | 컴포넌트 구성     |
| 4  | Flexbox 레이아웃   | 여러 요소 렌더링   |
| 5  | 조건부 스타일 적용     | `useState`  |

강의 시 추천 순서: 1\~4번으로 Tailwind의 유틸리티 클래스를 이해한 다음, 5번에서 React의 상태에 따라 CSS가 동적으로 변경되는 원리를 설명하면 효과적입니다.

모든 예제는 각각 `src/App.jsx`에 복사하여 실행할 수 있으며, `npm run dev`로 확인할 수 있습니다.
