# useCallback 사용 예시

`useCallback`은 **함수를 기억해 두었다가, 의존성 값이 바뀔 때만 새로 만드는 Hook**입니다.

컴포넌트가 다시 렌더링되면 그 안의 함수도 매번 **새로 만들어집니다**. 내용이 같아도 React는 "다른 함수"로 봅니다. 그래서 함수를 자식에게 넘기거나 `useEffect`의 의존성으로 쓸 때 불필요한 재실행이 생깁니다. `useCallback`은 이 문제를 막아 줍니다.

```jsx
const 기억된함수 = useCallback(() => { /* 내용 */ }, [의존성]);
```

대표적인 경우 6가지를 예시와 함께 정리했습니다.

---

## 1. memo로 감싼 자식 컴포넌트의 리렌더링 막기

가장 흔한 용도입니다. `memo`는 props가 같으면 자식을 다시 그리지 않는데, 함수 props가 매번 새로 만들어지면 소용이 없습니다.

```jsx
import { useState, useCallback, memo } from 'react';

function Parent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');

  // text를 입력해도 handleClick은 같은 함수로 유지됩니다
  const handleClick = useCallback(() => {
    setCount(c => c + 1);
  }, []);

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <p>count: {count}</p>
      <CountButton onClick={handleClick} />
    </div>
  );
}

const CountButton = memo(({ onClick }) => {
  console.log('CountButton 렌더링'); // 입력할 때는 찍히지 않습니다
  return <button onClick={onClick}>+1</button>;
});
```

## 2. useEffect의 의존성으로 함수를 쓸 때

`useEffect` 안에서 쓰는 함수를 의존성에 넣어야 할 때, `useCallback`이 없으면 렌더링할 때마다 effect가 다시 실행됩니다.

```jsx
import { useState, useEffect, useCallback } from 'react';

function SearchResult({ query }) {
  const [items, setItems] = useState([]);

  // query가 바뀔 때만 새 함수가 만들어집니다
  const fetchItems = useCallback(async () => {
    const res = await fetch(`https://dummyjson.com/products/search?q=${query}`);
    const data = await res.json();
    setItems(data.products);
  }, [query]);

  useEffect(() => {
    fetchItems();
  }, [fetchItems]); // fetchItems가 바뀔 때(= query가 바뀔 때)만 실행됩니다

  return (
    <div>
      <button onClick={fetchItems}>새로고침</button>
      <ul>{items.map(item => <li key={item.id}>{item.title}</li>)}</ul>
    </div>
  );
}
```

## 3. 함수형 업데이트로 의존성 줄이기

state를 직접 참조하면 그 state를 의존성에 넣어야 해서 함수가 자주 새로 만들어집니다. 함수형 업데이트(`prev => ...`)를 쓰면 의존성을 비울 수 있습니다.

```jsx
import { useState, useCallback, memo } from 'react';

function TodoApp() {
  const [todos, setTodos] = useState([]);
  const [input, setInput] = useState('');

  // ❌ todos가 바뀔 때마다 새 함수
  // const addTodo = useCallback(() => setTodos([...todos, input]), [todos, input]);

  // ✅ todos를 의존성에서 뺄 수 있습니다
  const removeTodo = useCallback((index) => {
    setTodos(prev => prev.filter((_, i) => i !== index));
  }, []);

  const addTodo = () => {
    setTodos(prev => [...prev, input]);
    setInput('');
  };

  return (
    <div>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={addTodo}>추가</button>
      <ul>
        {todos.map((todo, i) => (
          <TodoItem key={i} index={i} text={todo} onRemove={removeTodo} />
        ))}
      </ul>
    </div>
  );
}

const TodoItem = memo(({ index, text, onRemove }) => (
  <li>
    {text} <button onClick={() => onRemove(index)}>삭제</button>
  </li>
));
```

## 4. 커스텀 Hook에서 함수를 돌려줄 때

커스텀 Hook이 돌려주는 함수는 다른 컴포넌트의 의존성으로 쓰일 수 있으므로 `useCallback`으로 감싸 두는 것이 좋습니다.

```jsx
import { useState, useCallback } from 'react';

function useToggle(initial = false) {
  const [on, setOn] = useState(initial);

  const toggle = useCallback(() => setOn(v => !v), []);
  const turnOn = useCallback(() => setOn(true), []);
  const turnOff = useCallback(() => setOn(false), []);

  return { on, toggle, turnOn, turnOff };
}

// 사용
function Modal() {
  const { on, toggle, turnOff } = useToggle();

  return (
    <div>
      <button onClick={toggle}>모달 열기/닫기</button>
      {on && (
        <div className="modal">
          <p>모달 내용</p>
          <button onClick={turnOff}>닫기</button>
        </div>
      )}
    </div>
  );
}
```

## 5. Context로 함수를 내려줄 때

Provider의 `value`가 바뀌면 그 Context를 쓰는 모든 컴포넌트가 다시 렌더링됩니다. 함수는 `useCallback`, value 객체는 `useMemo`로 감싸서 불필요한 렌더링을 막습니다.

```jsx
import { createContext, useContext, useState, useCallback, useMemo } from 'react';

const CartContext = createContext(null);

function CartProvider({ children }) {
  const [items, setItems] = useState([]);

  const addItem = useCallback((product) => {
    setItems(prev => [...prev, product]);
  }, []);

  const clearCart = useCallback(() => setItems([]), []);

  const value = useMemo(
    () => ({ items, addItem, clearCart }),
    [items, addItem, clearCart]
  );

  return <CartContext.Provider value={value}>{children}</CartContext.Provider>;
}

function AddButton({ product }) {
  const { addItem } = useContext(CartContext);
  return <button onClick={() => addItem(product)}>장바구니 담기</button>;
}
```

## 6. 이벤트 리스너를 등록하고 해제할 때

`addEventListener`와 `removeEventListener`에는 **같은 함수**를 넘겨야 해제됩니다. 핸들러를 `useCallback`으로 고정해 effect가 불필요하게 다시 등록되지 않게 합니다.

```jsx
import { useState, useEffect, useCallback } from 'react';

function KeyboardCounter() {
  const [count, setCount] = useState(0);

  const handleKeyDown = useCallback((e) => {
    if (e.key === 'ArrowUp') setCount(c => c + 1);
    if (e.key === 'ArrowDown') setCount(c => c - 1);
  }, []);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [handleKeyDown]);

  return <p>↑/↓ 키를 눌러 보세요: {count}</p>;
}
```

---

## 정리

| 경우 | 의존성 배열 | 함께 쓰는 것 |
|---|---|---|
| 자식 리렌더링 방지 | `[]` | `memo` |
| useEffect 의존성 | `[query]` | `useEffect` |
| 함수형 업데이트 | `[]` | `setState(prev => ...)` |
| 커스텀 Hook 반환 함수 | `[]` | 커스텀 Hook |
| Context로 함수 전달 | `[]` | `useMemo`, `createContext` |
| 이벤트 리스너 | `[]` | `useEffect` |

## useCallback과 useMemo 비교

| 구분 | useCallback | useMemo |
|---|---|---|
| 기억하는 것 | **함수 자체** | 함수를 **실행한 결과 값** |
| 형태 | `useCallback(fn, deps)` | `useMemo(() => 값, deps)` |
| 같은 표현 | `useCallback(fn, deps)` | `useMemo(() => fn, deps)` |

## useCallback이 필요 없는 경우

- **자식이 `memo`로 감싸져 있지 않다면** 함수를 기억해도 자식은 어차피 다시 그려집니다. 효과가 없습니다.
- **일반 HTML 요소(`<button>`, `<input>`)에 넘기는 핸들러**는 감쌀 필요가 없습니다.
- 모든 함수를 감싸면 코드만 복잡해집니다. **성능 문제가 보이는 곳에만** 씁니다.
- React Compiler를 쓰는 프로젝트는 컴파일러가 자동으로 메모이제이션하므로 직접 쓸 일이 크게 줄어듭니다.
