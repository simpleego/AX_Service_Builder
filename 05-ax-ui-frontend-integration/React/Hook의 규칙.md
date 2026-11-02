#  Hook의 규칙
React 훅(Hook)의 핵심 규칙은 **“함수 컴포넌트나 커스텀 훅 안에서, 항상 같은 순서로 호출한다”**입니다. `useState`, `useEffect`, `useRef`, `useMemo`, `useCallback` 등에 적용됩니다.

**1. 훅을 호출할 수 있는 곳은 두 곳입니다**

| 호출 위치 | 가능 여부 |
|---|---|
| 함수 컴포넌트 본문 | ✅ |
| 커스텀 훅 본문 | ✅ |
| 일반 JavaScript 함수 | ❌ |
| 클래스 컴포넌트 | ❌ |
| 이벤트 처리 함수 | ❌ |
| `useEffect`, `useMemo` 등에 전달한 콜백 내부 | ❌ |

커스텀 훅은 `useCounter`, `useLogin`처럼 `use` 다음에 대문자로 시작하는 이름을 사용합니다. 커스텀 훅도 동일한 호출 규칙을 지켜야 합니다. [React](https://react.dev/reference/rules/rules-of-hooks?utm_source=chatgpt.com)

```jsx
import { useState } from "react";

// ✅ 커스텀 훅 내부에서 호출
function useCounter() {
  const [count, setCount] = useState(0);

  return { count, setCount };
}

// ✅ 함수 컴포넌트 내부에서 호출
function Counter() {
  const { count, setCount } = useCounter();

  return (
    <button onClick={() => setCount(c => c + 1)}>
      {count}
    </button>
  );
}
```

여기서 **`setCount()`는 훅이 반환한 상태 변경 함수**이므로 이벤트 처리 함수에서 호출해도 됩니다. `useState()` 자체를 이벤트 안에서 호출하면 안 됩니다.

**2. 훅은 함수의 최상위에서 호출합니다**

여기서 **최상위란 파일 맨 위가 아니라, 컴포넌트 또는 커스텀 훅의 본문에서 다른 블록이나 함수에 감싸지지 않은 위치**를 뜻합니다.

조건문·반복문·중첩 함수·`try/catch/finally` 안에서는 호출하면 안 됩니다. 조건부 `return`보다 뒤에 배치하는 것도 금지됩니다. [React](https://react.dev/reference/rules/rules-of-hooks?utm_source=chatgpt.com)

```jsx
// ❌ 잘못된 예
function Profile({ isLoggedIn }) {
  if (isLoggedIn) {
    const [name, setName] = useState("");
  }

  return <div>프로필</div>;
}
```

```jsx
// ✅ 올바른 예
function Profile({ isLoggedIn }) {
  const [name, setName] = useState("");

  if (!isLoggedIn) {
    return <p>로그인이 필요합니다.</p>;
  }

  return (
    <input
      value={name}
      onChange={e => setName(e.target.value)}
    />
  );
}
```

**3. 조건에 따라 동작시키려면, 훅 내부의 로직에 조건을 둡니다**

`useEffect`를 조건부로 호출하는 대신, `useEffect`에 전달하는 함수 안에서 조건을 검사합니다. [React](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks?utm_source=chatgpt.com)

```jsx
// ❌ 조건에 따라 훅 호출 자체가 달라짐
if (isLoggedIn) {
  useEffect(() => {
    console.log("로그인 상태입니다.");
  }, []);
}
```

```jsx
// ✅ 훅은 항상 호출하고, 실행할 작업만 조건으로 제어
useEffect(() => {
  if (isLoggedIn) {
    console.log("로그인 상태입니다.");
  }
}, [isLoggedIn]);
```

**4. 이러한 규칙이 필요한 이유는 ‘호출 순서’입니다**

React는 훅의 호출 순서를 이용해 이전 렌더링의 상태와 현재 렌더링의 상태를 연결합니다. 조건에 따라 훅이 생략되면 연결이 어긋날 수 있습니다. [React](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks?utm_source=chatgpt.com)

```jsx
const [name, setName] = useState("");    // 첫 번째 훅
const [age, setAge] = useState(0);       // 두 번째 훅
const inputRef = useRef(null);          // 세 번째 훅
```

| 렌더링 | 첫 번째 호출 | 두 번째 호출 | 세 번째 호출 |
|---|---|---|---|
| 첫 렌더링 | 이름 상태 | 나이 상태 | 입력 요소 참조 |
| 다음 렌더링 | 이름 상태 | 나이 상태 | 입력 요소 참조 |

학생들에게는 **“React가 매번 같은 순서의 보관함을 찾아가므로, 중간 보관함을 조건에 따라 빼면 안 된다”**라고 설명할 수 있습니다.

**5. 예외: React 19의 `use()`**

`use()`는 특별히 **조건문과 반복문 안에서 호출할 수 있습니다.** 다만 컴포넌트 또는 커스텀 훅 안에서 호출해야 하며, `try/catch`로 감싸면 안 됩니다. 이 예외는 `useState`, `useEffect` 등에 적용되지 않습니다. [React](https://react.dev/reference/eslint-plugin-react-hooks/lints/rules-of-hooks?utm_source=chatgpt.com)

실습에서는 `eslint-plugin-react-hooks`를 활용하면 훅의 호출 규칙 위반을 자동으로 확인할 수 있습니다. [React](https://react.dev/reference/rules/rules-of-hooks?utm_source=chatgpt.com)
