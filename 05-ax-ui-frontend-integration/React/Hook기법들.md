# Hook의 3가지 기법
- useMemo
- useCallback
- useRef

세 훅 모두 **렌더링이 반복되어도 무언가를 유지하기 위해** 씁니다. 컴포넌트 함수는 렌더링마다 처음부터 다시 실행되고, 그 안의 변수와 함수도 매번 새로 만들어집니다. 그래서 무엇을 유지하느냐에 따라 훅이 나뉩니다.

| 훅 | 유지하는 것 | 없으면 생기는 문제 |
|---|---|---|
| `useMemo` | 계산 결과(값) | 무거운 계산이 렌더링마다 반복됨 |
| `useCallback` | 함수 | 자식 컴포넌트가 불필요하게 다시 그려짐 |
| `useRef` | 아무 값(`.current`)이나 DOM 요소 | 값을 유지하려면 State를 써야 해서 재렌더링이 생김 |

---

## 1. useMemo: 계산 결과를 기억

**상황:** 상품 10,000개를 검색어로 거르는 화면에 다크 모드 버튼이 있습니다.

```jsx
import { useState, useMemo } from "react";

const products = Array.from({ length: 10000 }, (_, i) => `상품 ${i}`);

function filterProducts(list, keyword) {
  console.log("필터링 실행!"); // 몇 번 실행되는지 확인용
  return list.filter((p) => p.includes(keyword));
}

export default function ProductList() {
  const [keyword, setKeyword] = useState("");
  const [dark, setDark] = useState(false);

  // ❌ useMemo 없이: 다크 모드만 바꿔도 10,000개를 다시 거름
  // const filtered = filterProducts(products, keyword);

  // ✅ keyword가 바뀔 때만 다시 계산하고, 아니면 이전 결과를 재사용
  const filtered = useMemo(
    () => filterProducts(products, keyword),
    [keyword]
  );

  return (
    <div style={{ background: dark ? "#222" : "#fff", color: dark ? "#fff" : "#000" }}>
      <input value={keyword} onChange={(e) => setKeyword(e.target.value)} />
      <button onClick={() => setDark(!dark)}>테마 변경</button>
      <p>결과 {filtered.length}개</p>
    </div>
  );
}
```

**왜 필요한가**
- 다크 모드를 바꾸면 `ProductList` 함수 전체가 다시 실행됩니다.
- useMemo가 없으면 검색어는 그대로인데도 필터링이 매번 다시 돕니다. 콘솔에 "필터링 실행!"이 계속 찍힙니다.
- useMemo를 쓰면 의존성 배열 `[keyword]`가 같을 때 이전 결과를 그대로 돌려줍니다.
- **주의:** useMemo 안의 함수는 렌더링 중에 실행됩니다. 그래서 API 호출 같은 사이드 이펙트는 넣지 말고 `useEffect`에 넣어야 합니다.

---

## 2. useCallback: 함수 자체를 기억

**상황:** 부모에 카운터가 있고, 무거운 자식 컴포넌트에 클릭 핸들러를 넘깁니다.

```jsx
import { useState, useCallback, memo } from "react";

// memo: props가 같으면 다시 그리지 않는 컴포넌트
const HeavyButton = memo(function HeavyButton({ onClick, label }) {
  console.log(`${label} 버튼 렌더링`);
  return <button onClick={onClick}>{label}</button>;
});

export default function Parent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  // ❌ useCallback 없이: 렌더링마다 새 함수가 만들어짐
  // const handleReset = () => setCount(0);

  // ✅ 한 번 만든 함수를 계속 재사용
  const handleReset = useCallback(() => setCount(0), []);

  return (
    <div>
      <p>count: {count}</p>
      <button onClick={() => setCount((c) => c + 1)}>+1</button>
      <input value={text} onChange={(e) => setText(e.target.value)} />
      <HeavyButton onClick={handleReset} label="초기화" />
    </div>
  );
}
```

**왜 필요한가**
- 자바스크립트에서 함수는 객체입니다. 내용이 똑같아도 새로 만들면 `이전 함수 !== 새 함수`가 됩니다.
- 입력창에 글자를 칠 때마다 `Parent`가 다시 렌더링되고 `handleReset`도 새로 만들어집니다. `memo`는 props가 바뀌었다고 판단해서 `HeavyButton`을 매번 다시 그립니다. 결국 `memo`를 쓴 의미가 없어집니다.
- useCallback으로 같은 함수를 유지하면 props가 그대로이므로 `HeavyButton`이 다시 그려지지 않습니다.
- 슬라이드의 `useCallback(fn, deps) === useMemo(() => fn, deps)`가 바로 이 뜻입니다. **함수를 값으로 기억하는 useMemo**라고 보면 됩니다.
- **주의:** 받는 쪽이 `memo` 컴포넌트이거나, 그 함수가 `useEffect`의 의존성에 들어갈 때만 효과가 있습니다. 그 외에는 굳이 쓸 필요가 없습니다.

---

## 3. useRef: 바뀌어도 조용한 상자

**상황:** 스톱워치입니다. `setInterval`의 ID를 저장해 두었다가 정지할 때 써야 하고, 시작하면 입력창에 포커스도 줍니다.

```jsx
import { useState, useRef } from "react";

export default function Stopwatch() {
  const [seconds, setSeconds] = useState(0);
  const timerId = useRef(null);   // ① 값 보관용: 바뀌어도 재렌더링 없음
  const inputRef = useRef(null);  // ② DOM 접근용

  const start = () => {
    if (timerId.current) return;            // 이미 실행 중이면 무시
    timerId.current = setInterval(() => {
      setSeconds((s) => s + 1);
    }, 1000);
    inputRef.current.focus();               // 실제 <input> DOM 요소에 접근
  };

  const stop = () => {
    clearInterval(timerId.current);         // 저장해 둔 ID로 정지
    timerId.current = null;
  };

  return (
    <div>
      <h2>{seconds}초</h2>
      <button onClick={start}>시작</button>
      <button onClick={stop}>정지</button>
      <input ref={inputRef} placeholder="기록 메모" />
    </div>
  );
}
```

**왜 필요한가.** 타이머 ID를 다른 방법으로 저장하면 이렇게 됩니다.

| 저장 방법 | 결과 |
|---|---|
| `let timerId` (일반 변수) | 1초마다 재렌더링되면서 함수가 다시 실행되어 `null`로 초기화됩니다. **정지 버튼이 작동하지 않습니다.** |
| `useState` | 값은 유지되지만 ID를 저장할 때마다 화면에 쓰지도 않는 값 때문에 재렌더링이 생깁니다. |
| `useRef` | 값이 렌더링 사이에 유지되고, 바꿔도 재렌더링이 없습니다. ✅ |

- `ref={inputRef}`로 연결하면 `inputRef.current`가 실제 `<input>` DOM 요소가 됩니다. `focus()`, 스크롤 위치 조정, 크기 측정처럼 리액트가 직접 해 주지 않는 DOM 작업에 씁니다.
- 판단 기준: **화면에 보여야 하는 값은 `useState`, 화면과 무관하게 기억만 하면 되는 값은 `useRef`** 입니다.

---

## 한눈에 정리

- **useMemo**: "이 계산, 입력이 같으면 다시 하지 마" → 성능 최적화
- **useCallback**: "이 함수, 매번 새로 만들지 마" → `memo` 자식의 불필요한 렌더링 방지
- **useRef**: "이 값은 기억만 하고, 바뀌어도 화면은 다시 그리지 마" → 타이머 ID, 이전 값, DOM 요소 보관

useMemo와 useCallback은 **성능 최적화 도구**라서 문제가 생길 때 쓰는 것이 원칙입니다. 반면 useRef는 위 스톱워치처럼 **없으면 기능이 동작하지 않는** 경우가 있습니다.
