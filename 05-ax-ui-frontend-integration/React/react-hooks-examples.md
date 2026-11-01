# React Hook 예시 소스 코드

"React Hook 핵심 메서드 가이드" 문서에 들어 있는 예시 코드 모음입니다.

## 1. useState: 상태 관리

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

## 2. useEffect: 부수 효과 처리

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

## 3. useRef: DOM 접근과 값 보관

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

## 4. useMemo / useCallback: 메모이제이션

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

## 5. useContext: 전역 값 공유

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

## 7. 커스텀 Hook: useFetch

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
