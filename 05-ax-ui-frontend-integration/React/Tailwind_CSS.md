# React에서 Tailwind CSS 활용하기 — 실습 예제 5개

Tailwind CSS는 별도의 CSS 파일에 스타일을 일일이 작성하는 대신, JSX의 `className`에 미리 정의된 유틸리티 클래스를 조합하여 디자인하는 CSS 프레임워크입니다.

React 입문자가 Tailwind CSS의 주요 기능을 단계적으로 학습할 수 있도록 실무에서 자주 사용하는 5가지 예제를 작성했습니다.

| 예제 | 실습 주제    | 핵심 학습 내용                  |
| -- | -------- | ------------------------- |
| 1  | 버튼 디자인   | 색상, 크기, 여백, Hover         |
| 2  | 상품 카드    | Flexbox, 그림자, 배지          |
| 3  | 반응형 대시보드 | Grid, 반응형 브레이크포인트         |
| 4  | 로그인 폼    | 입력 필드, Focus, React State |
| 5  | 다크 모드    | 조건부 스타일, 테마 전환            |

## 0. React + Tailwind CSS 설치

현재 공식 Tailwind CSS v4 기준으로 Vite와 React를 사용하는 방법입니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://tailwindcss.com\&sz=32)

Tailwind CSS



① React 프로젝트 생성

```
npm create vite@latest tailwind-practice -- --template react

cd tailwind-practice

npm install
```

② Tailwind CSS 설치

```
npm install tailwindcss @tailwindcss/vite
```

③ `vite.config.js` 수정

```
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

④ `src/index.css` 수정

```
@import "tailwindcss";
```

⑤ `src/main.jsx`에서 CSS 불러오기

```
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
```

실행:

```
npm run dev
```

이제 아래 예제 중 하나를 `src/App.jsx`에 복사하면 실행할 수 있습니다.

## 예제 1. 다양한 스타일의 버튼 만들기

실행 화면 예시

기본 버튼

성공 버튼

삭제 버튼

테두리 버튼

학습 목표: `bg-*`, `text-*`, `px-*`, `py-*`, `rounded-*`, `hover:*` 사용법

```

export default function App() {
  return (
    <div className="p-10 space-y-5">
      <h1 className="text-2xl font-bold">
        Tailwind 버튼 예제
      </h1>

      <div className="flex flex-wrap gap-4">

        {/* 기본 버튼 */}
        <button
          className="bg-blue-600 text-white
                     px-5 py-2 rounded-lg
                     hover:bg-blue-800
                     transition-colors"
        >
          기본 버튼
        </button>

        {/* 성공 버튼 */}
        <button
          className="bg-green-600 text-white
                     px-5 py-2 rounded-lg
                     hover:bg-green-700"
        >
          성공 버튼
        </button>

        {/* 삭제 버튼 */}
        <button
          className="bg-red-600 text-white
                     px-5 py-2 rounded-lg
                     hover:bg-red-700"
        >
          삭제 버튼
        </button>

        {/* 테두리 버튼 */}
        <button
          className="border-2 border-blue-600
                     text-blue-600 px-5 py-2
                     rounded-lg
                     hover:bg-blue-50"
        >
          테두리 버튼
        </button>

      </div>
    </div>
  );
}

```

주요 Tailwind 클래스:

| 클래스                 | 역할                |
| ------------------- | ----------------- |
| `bg-blue-600`       | 파란색 배경            |
| `text-white`        | 흰색 글자             |
| `px-5 py-2`         | 가로·세로 내부 여백       |
| `rounded-lg`        | 둥근 모서리            |
| `hover:bg-blue-800` | 마우스를 올리면 배경 변경    |
| `transition-colors` | 색상이 부드럽게 변경       |
| `flex gap-4`        | 버튼을 가로 배치하고 간격 지정 |

핵심은 `hover:`처럼 접두사를 붙이면 특정 상태에서만 스타일을 적용할 수 있다는 것입니다.

## 예제 2. 쇼핑몰 상품 카드 만들기

[White sneaker](https://images.openai.com/static-rsc-4/MfA0JmUua0GVReb7DGvkRU_2ReelpVmXtnkAF-NG8v-172WPoNurfwok5Y1pf26shOIiChTN2HVbupKp5VuzTqjAPwPnUMdCK-XrrLN5raCjCW-GK_-xBfQ_8IL1Xsxgt9UF68nOnC6zsXevf6WJjTlzkcalUOXFoeJxZwY_e54ypRTBvsaGy4sWiG6TZAoU?purpose=inline)

러닝 운동화

BEST

가볍고 편안한 데일리 운동화

## 59,000원

장바구니 담기

학습 목표: 카드 레이아웃, Flexbox, 그림자, 배지, React 이벤트 처리

```

export default function App() {
  const product = {
    name: "러닝 운동화",
    price: 59000,
    description: "가볍고 편안한 데일리 운동화",
    image: "https://placehold.co/400x250?text=Shoes",
  };

  const addToCart = () => {
    alert(`${product.name} 장바구니에 추가!`);
  };

  return (
    <div className="min-h-screen bg-gray-100 p-10">

      {/* 상품 카드 */}
      <div
        className="w-80 bg-white rounded-xl
                   shadow-lg overflow-hidden
                   hover:shadow-2xl
                   transition-shadow"
      >
        {/* 상품 이미지 */}
        <img
          src={product.image}
          alt={product.name}
          className="w-full h-48 object-cover"
        />

        <div className="p-5 space-y-3">
          <span
            className="bg-green-100 text-green-700
                       text-xs px-3 py-1 rounded-full"
          >
            BEST
          </span>

          <h2 className="text-xl font-bold">
            {product.name}
          </h2>

          <p className="text-gray-500 text-sm">
            {product.description}
          </p>

          <div className="flex justify-between items-center">
            <span className="text-lg font-bold">
              {product.price.toLocaleString()}원
            </span>

            <button
              onClick={addToCart}
              className="bg-blue-600 text-white
                         px-4 py-2 rounded-lg
                         hover:bg-blue-700"
            >
              담기
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

```

주요 Tailwind 클래스:

| 클래스                    | 역할                  |
| ---------------------- | ------------------- |
| `w-80`                 | 너비 20rem            |
| `shadow-lg`            | 카드에 그림자 적용          |
| `overflow-hidden`      | 카드 밖으로 넘치는 내용 숨김    |
| `object-cover`         | 이미지 비율을 유지하며 영역 채우기 |
| `flex justify-between` | 양쪽 끝으로 요소 배치        |
| `items-center`         | 수직 방향 중앙 정렬         |
| `space-y-3`            | 자식 요소 사이 세로 간격      |

React와 Tailwind의 역할 구분: 상품 데이터와 장바구니 이벤트는 React가 처리하고, 상품 카드의 디자인은 Tailwind CSS가 담당합니다.

## 예제 3. 반응형 관리자 대시보드 만들기

데스크톱 화면 예시

관리자 대시보드

전체 사용자

1,250명

오늘 주문

85건

매출액

3,500,000원

화면 너비에 따라 카드가 1열 → 2열 → 3열로 재배치됩니다.

학습 목표: `grid`, `grid-cols-*`, `md:*`, `lg:*`로 반응형 웹 구현

```

export default function App() {
  const stats = [
    { title: "전체 사용자", value: "1,250명", icon: "👥" },
    { title: "오늘 주문", value: "85건", icon: "🛒" },
    { title: "매출액", value: "3,500,000원", icon: "💰" },
  ];

  return (
    <div className="min-h-screen bg-gray-100">

      {/* 상단 헤더 */}
      <header className="bg-slate-800 text-white p-5">
        <h1 className="text-2xl font-bold">
          관리자 대시보드
        </h1>
      </header>

      <main className="max-w-6xl mx-auto p-6">

        <h2 className="text-xl font-semibold mb-5">
          서비스 현황
        </h2>

        {/* 반응형 카드 배치 */}
        <div
          className="grid grid-cols-1
                     md:grid-cols-2
                     lg:grid-cols-3 gap-6"
        >
          {stats.map((item) => (
            <div
              key={item.title}
              className="bg-white p-6
                         rounded-xl shadow-md
                         hover:shadow-lg"
            >
              <div className="text-3xl mb-3">
                {item.icon}
              </div>

              <p className="text-gray-500">
                {item.title}
              </p>

              <p className="text-2xl font-bold mt-2">
                {item.value}
              </p>
            </div>
          ))}
        </div>

      </main>
    </div>
  );
}

```

반응형 클래스의 동작:

| 브라우저 너비   | 적용 클래스           | 카드 배치 |
| --------- | ---------------- | ----- |
| 768px 미만  | `grid-cols-1`    | 1열    |
| 768px 이상  | `md:grid-cols-2` | 2열    |
| 1024px 이상 | `lg:grid-cols-3` | 3열    |

Tailwind는 모바일 우선(Mobile First) 방식을 사용합니다.

즉, `md:`는 화면 너비가 768px 이상일 때 해당 스타일을 적용한다는 의미입니다.

## 예제 4. React State와 Tailwind로 로그인 폼 만들기

## 로그인

이메일

비밀번호

로그인

학습 목표: React `useState`, 입력값 관리, Focus 스타일, 폼 이벤트

```

import { useState } from "react";

export default function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    // 서버 인증 없이 입력값만 확인하는 예제
    alert(`로그인 요청 이메일: ${email}`);
  };

  return (
    <div
      className="min-h-screen bg-gray-100
                 flex items-center justify-center"
    >
      <form
        onSubmit={handleSubmit}
        className="bg-white p-8 rounded-xl
                   shadow-lg w-full max-w-sm"
      >
        <h1
          className="text-2xl font-bold
                     text-center mb-6"
        >
          로그인
        </h1>

        {/* 이메일 입력 */}
        <label className="block mb-2 text-sm font-medium">
          이메일
        </label>

        <input
          type="email"
          required
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="example@email.com"
          className="w-full border border-gray-300
                     rounded-lg px-4 py-3 mb-4
                     focus:outline-none
                     focus:ring-2
                     focus:ring-blue-500"
        />

        {/* 비밀번호 입력 */}
        <label className="block mb-2 text-sm font-medium">
          비밀번호
        </label>

        <input
          type="password"
          required
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="비밀번호 입력"
          className="w-full border border-gray-300
                     rounded-lg px-4 py-3 mb-6
                     focus:outline-none
                     focus:ring-2
                     focus:ring-blue-500"
        />

        <button
          type="submit"
          className="w-full bg-blue-600 text-white
                     py-3 rounded-lg font-semibold
                     hover:bg-blue-700"
        >
          로그인
        </button>
      </form>
    </div>
  );
}

```

특히 중요한 클래스는 다음과 같습니다.

- `focus:ring-2`: 입력창을 선택하면 두께가 있는 포커스 링 표시
- `focus:ring-blue-500`: 포커스 링의 색상 지정
- `focus:outline-none`: 브라우저 기본 외곽선 제거 (대신 포커스 링 제공)
- `max-w-sm`: 로그인 창의 최대 너비 제한
- `min-h-screen`: 화면 전체 높이를 최소 높이로 지정

이 예제는 로그인 UI와 입력값 관리까지만 구현합니다. 실제 인증은 FastAPI 등의 백엔드와 연결해야 합니다.

## 예제 5. 다크 모드 전환 기능 만들기

라이트 모드

다크 모드 전환

React + Tailwind CSS

버튼을 클릭하면 테마에 따라 배경색과 글자색이 변경됩니다.

학습 목표: React 상태에 따른 조건부 스타일과 `dark:` 클래스

Tailwind CSS v4에서 수동으로 다크 모드를 전환하려면 CSS에 사용자 정의 `dark` 변형을 선언할 수 있습니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://tailwindcss.com\&sz=32)

Tailwind CSS



① `src/index.css`

```
@import "tailwindcss";

@custom-variant dark (&:where(.dark, .dark *));
```

② `src/App.jsx`

```

import { useState } from "react";

export default function App() {
  const [darkMode, setDarkMode] = useState(false);

  return (
    <div className={darkMode ? "dark" : ""}>
      <div
        className="min-h-screen
                   bg-gray-100 text-gray-900
                   dark:bg-gray-900 dark:text-white
                   flex items-center justify-center"
      >
        <div
          className="bg-white dark:bg-gray-800
                     p-10 rounded-xl shadow-lg
                     text-center"
        >
          <h1 className="text-2xl font-bold mb-5">
            React + Tailwind CSS
          </h1>

          <p
            className="text-gray-600
                       dark:text-gray-300 mb-6"
          >
            현재 모드:
            {darkMode ? " 다크 모드" : " 라이트 모드"}
          </p>

          <button
            onClick={() => setDarkMode(!darkMode)}
            className="bg-blue-600 text-white
                       px-6 py-3 rounded-lg
                       hover:bg-blue-700"
          >
            {darkMode
              ? "라이트 모드 전환"
              : "다크 모드 전환"}
          </button>
        </div>
      </div>
    </div>
  );
}

```

핵심 코드:

```
<div className="bg-white dark:bg-gray-800">
```

- 기본 상태에서는 `bg-white` 적용
- 상위 요소에 `dark` 클래스가 있으면 `dark:bg-gray-800` 적용
- React의 `darkMode` 상태가 변경되면 해당 클래스의 적용 여부도 변경

따라서 React는 언제 테마를 변경할지 결정하고, Tailwind CSS는 어떻게 보여줄지 결정합니다.

## 6. 다섯 예제로 학습하는 Tailwind CSS 핵심 문법

| 구분      | 예시 클래스              | 의미            |
| ------- | ------------------- | ------------- |
| 배경색     | `bg-blue-500`       | 배경을 파란색으로     |
| 글자색     | `text-red-600`      | 글자를 빨간색으로     |
| 글자 크기   | `text-xl`           | 큰 글자          |
| 글자 두께   | `font-bold`         | 굵게            |
| 내부 여백   | `p-4`               | 상하좌우 패딩       |
| 외부 여백   | `m-4`               | 상하좌우 마진       |
| 너비      | `w-full`            | 부모 너비 100%    |
| 높이      | `h-40`              | 높이 10rem      |
| Flexbox | `flex`              | Flex 레이아웃     |
| Grid    | `grid grid-cols-3`  | 3열 Grid       |
| 모서리     | `rounded-lg`        | 둥근 모서리        |
| 그림자     | `shadow-md`         | 중간 크기 그림자     |
| Hover   | `hover:bg-blue-700` | 마우스 오버 시 변경   |
| Focus   | `focus:ring-2`      | 포커스 시 링 표시    |
| 반응형     | `md:grid-cols-2`    | 768px 이상에서 2열 |
| 다크 모드   | `dark:bg-gray-900`  | 다크 모드일 때 배경색  |

## 7. React 교육에서 강조할 핵심 개념

일반 CSS와 Tailwind CSS의 차이를 동일한 버튼으로 비교하면 이해하기 쉽습니다.

일반 CSS

버튼

JSX와 CSS 파일을 따로 작성

Tailwind CSS

버튼

JSX의 className에 스타일 조합

일반 CSS 방식

```
<button className="my-button">버튼</button>
```

```
.my-button {
  background-color: #2563eb;
  color: white;
  padding: 8px 16px;
  border-radius: 8px;
}
```

Tailwind CSS 방식

```
<button
  className="bg-blue-600 text-white px-4 py-2 rounded-lg"
>
  버튼
</button>
```

Tailwind CSS는 React의 상태관리, 이벤트 처리, 컴포넌트 구조를 대체하지 않습니다. 스타일링 방식을 바꿔 주는 도구입니다.

추천 학습 순서: 버튼 → 상품 카드 → 반응형 레이아웃 → 로그인 폼 → 다크 모드

이 순서라면 단순 스타일링부터 React State와 연동한 동적 UI까지 자연스럽게 학습할 수 있습니다.

참고 자료: [Tailwind CSS 공식 설치 문서](https://tailwindcss.com/docs/installation/using-vite?utm_source=chatgpt.com) · [Tailwind CSS Utility-First 개념](https://tailwindcss.com/docs/utility-first?utm_source=chatgpt.com)
