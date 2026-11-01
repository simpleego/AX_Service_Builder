# React Hook 핵심 메서드 가이드

Nov 2, 2026 · @Jong Cheon Park

## 0. Hook이란?

Hook은 **함수형 컴포넌트에서 상태(state)와 생명주기 같은 React 기능을 쓰게 해 주는 함수**입니다. 이름은 항상 `use`로 시작합니다.

**지켜야 할 규칙 2가지**

1. **컴포넌트 최상단에서만 호출합니다.** 반복문, 조건문, 중첩 함수 안에서는 호출하지 않습니다.
2. **React 함수 컴포넌트나 커스텀 Hook 안에서만 호출합니다.**

## 1. useState: 상태 관리

값이 바뀌면 화면을 다시 그려야 할 때 씁니다.

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0); // [현재값, 변경함수] = useState(초기값)

  return (
    <div>
      <p>현재 값: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      {/* 이전 값을 기준으로 바꿀 때는 함수형 업데이트가 안전합니다 */}
      <button onClick={() => setCount(prev => prev - 1)}>-1</button>
    </div>
  );
}
```

> 💡 객체나 배열 상태는 **새 객체를 만들어서** 바꿔야 합니다. `setUser({ ...user, name: '철수' })` ✅ / `user.name = '철수'` ❌

## 2. useEffect: 부수 효과 처리

렌더링이 끝난 **뒤에** 실행할 작업에 씁니다. API 호출, 타이머, 이벤트 구독 같은 것들입니다.

```jsx
import { useState, useEffect } from 'react';

function Timer() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    const id = setInterval(() => setSeconds(s => s + 1), 1000);

    // cleanup: 컴포넌트가 사라지거나 effect가 다시 실행되기 전에 호출됩니다
    return () => clearInterval(id);
  }, []); // 의존성 배열

  return <p>{seconds}초 경과</p>;
}
```

| 의존성 배열 | 실행 시점 |
| --- | --- |
| 생략 | 렌더링할 때마다 |
| `[]` | 처음 마운트될 때 한 번 |
| `[a, b]` | 처음 마운트될 때 + `a`나 `b`가 바뀔 때 |

## 3. useRef: DOM 접근과 값 보관

- DOM 요소를 직접 다룰 때 씁니다(포커스, 스크롤 등).
- 바뀌어도 **화면을 다시 그리지 않는 값**을 보관할 때 씁니다.

```jsx
import { useRef } from 'react';

function FocusInput() {
  const inputRef = useRef(null);
  const clickCount = useRef(0); // 값이 바뀌어도 리렌더링되지 않습니다

  const handleClick = () => {
    inputRef.current.focus();   // .current로 접근합니다
    clickCount.current += 1;
    console.log(`클릭 ${clickCount.current}번`);
  };

  return (
    <>
      <input ref={inputRef} />
      <button onClick={handleClick}>입력창 포커스</button>
    </>
  );
}
```

## 4. useMemo / useCallback: 메모이제이션(성능 최적화)

- `useMemo`: 계산 **결과 값**을 기억합니다.
- `useCallback`: **함수 자체**를 기억합니다.

```jsx
import { useState, useMemo, useCallback, memo } from 'react';

function ProductList({ products }) {
  const [keyword, setKeyword] = useState('');
  const [dark, setDark] = useState(false);

  // keyword나 products가 바뀔 때만 다시 계산합니다 (dark를 바꿀 때는 재계산하지 않음)
  const filtered = useMemo(() => {
    console.log('필터링 실행');
    return products.filter(p => p.name.includes(keyword));
  }, [products, keyword]);

  // 렌더링될 때마다 새 함수가 만들어지지 않게 합니다
  const handleSelect = useCallback((id) => {
    console.log('선택:', id);
  }, []);

  return (
    <div className={dark ? 'dark' : ''}>
      <input value={keyword} onChange={e => setKeyword(e.target.value)} />
      <button onClick={() => setDark(d => !d)}>테마 전환</button>
      {filtered.map(p => <Item key={p.id} item={p} onSelect={handleSelect} />)}
    </div>
  );
}

// memo + useCallback을 함께 써야 자식 컴포넌트의 불필요한 리렌더링을 막을 수 있습니다
const Item = memo(({ item, onSelect }) => (
  <li onClick={() => onSelect(item.id)}>{item.name}</li>
));
```

> 💡 모든 곳에 쓰지 마세요. **계산이 무겁거나, memo로 감싼 자식에게 넘길 때** 효과가 있습니다.

## 5. useContext: 전역 값 공유

props를 여러 단계로 계속 넘기는 문제(props drilling) 없이 값을 공유합니다.

```jsx
import { createContext, useContext, useState } from 'react';

const ThemeContext = createContext('light'); // 1) Context 만들기

function App() {
  const [theme, setTheme] = useState('light');
  return (
    // 2) Provider로 값 내려주기
    <ThemeContext.Provider value={{ theme, setTheme }}>
      <Toolbar />
    </ThemeContext.Provider>
  );
}

function Toolbar() {
  return <ThemeButton />; // 중간 컴포넌트는 props를 넘길 필요가 없습니다
}

function ThemeButton() {
  const { theme, setTheme } = useContext(ThemeContext); // 3) 어디서든 꺼내 쓰기
  return (
    <button onClick={() => setTheme(theme === 'light' ? 'dark' : 'light')}>
      현재 테마: {theme}
    </button>
  );
}
```

## 6. useReducer: 복잡한 상태 로직

상태를 바꾸는 방법이 여러 가지일 때, 그 로직을 한곳(reducer)에 모읍니다.

```jsx
import { useReducer } from 'react';

const initialState = { count: 0, step: 1 };

function reducer(state, action) {
  switch (action.type) {
    case 'increment': return { ...state, count: state.count + state.step };
    case 'decrement': return { ...state, count: state.count - state.step };
    case 'setStep':   return { ...state, step: action.payload };
    case 'reset':     return initialState;
    default: throw new Error('알 수 없는 액션');
  }
}

function StepCounter() {
  const [state, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <p>{state.count} (단위: {state.step})</p>
      <button onClick={() => dispatch({ type: 'increment' })}>+</button>
      <button onClick={() => dispatch({ type: 'decrement' })}>-</button>
      <input
        type="number"
        value={state.step}
        onChange={e => dispatch({ type: 'setStep', payload: Number(e.target.value) })}
      />
      <button onClick={() => dispatch({ type: 'reset' })}>초기화</button>
    </div>
  );
}
```

## 7. 커스텀 Hook: 로직 재사용

반복되는 Hook 로직을 `use`로 시작하는 함수로 빼서 재사용합니다.

```jsx
import { useState, useEffect } from 'react';

function useFetch(url) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let ignore = false; // 이전 요청 응답이 늦게 도착하는 경우를 막습니다
    setLoading(true);

    fetch(url)
      .then(res => res.json())
      .then(json => { if (!ignore) setData(json); })
      .catch(err => { if (!ignore) setError(err); })
      .finally(() => { if (!ignore) setLoading(false); });

    return () => { ignore = true; };
  }, [url]);

  return { data, loading, error };
}

// 사용
function UserList() {
  const { data, loading, error } = useFetch('https://jsonplaceholder.typicode.com/users');

  if (loading) return <p>로딩 중...</p>;
  if (error) return <p>에러 발생!</p>;
  return <ul>{data.map(u => <li key={u.id}>{u.name}</li>)}</ul>;
}
```

## 8. 한눈에 보는 요약

| Hook | 용도 | 한 줄 요약 |
| --- | --- | --- |
| useState | 상태 | 값이 바뀌면 화면을 다시 그립니다 |
| useEffect | 부수 효과 | 렌더링 후 실행하고 cleanup으로 정리합니다 |
| useRef | DOM, 값 보관 | 바뀌어도 리렌더링되지 않습니다 |
| useMemo | 값 캐싱 | 무거운 계산 결과를 기억합니다 |
| useCallback | 함수 캐싱 | 함수가 새로 만들어지지 않게 합니다 |
| useContext | 전역 공유 | props drilling 없이 값을 꺼내 씁니다 |
| useReducer | 복잡한 상태 | 상태 변경 로직을 reducer 한곳에 모읍니다 |
| 커스텀 Hook | 재사용 | 반복되는 Hook 로직을 함수로 묶습니다 |

**추천 학습 순서:** useState → useEffect → useRef → useContext → useReducer → useMemo/useCallback → 커스텀 Hook
