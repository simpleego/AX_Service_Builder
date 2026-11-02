Todo 앱에서 활용하기 좋은 커스텀 훅을 **저장·할 일 관리·필터링**의 3가지 역할로 나누겠습니다.

아래는 **Vite 기반 React 앱에서 서버 없이 동작하는 예제**입니다.

| 커스텀 훅 | 역할 | 사용하는 훅 |
|---|---|---|
| `useLocalStorage` | 새로고침해도 데이터 유지 | `useState`, `useEffect` |
| `useTodos` | 할 일 추가·완료 전환·삭제 | `useLocalStorage` |
| `useTodoFilter` | 전체·미완료·완료 필터링 | `useState` |

**① `useLocalStorage` — 데이터를 브라우저에 저장**

`src/hooks/useLocalStorage.js`

```javascript
import { useEffect, useState } from "react";

// key는 사용 중 바뀌지 않는 고정된 문자열로 전달합니다.
// initialValue는 JSON으로 저장 가능한 값을 사용합니다.
export default function useLocalStorage(key, initialValue) {
  // 최초 렌더링 시 저장된 데이터를 읽습니다.
  const [value, setValue] = useState(() => {
    try {
      const saved = localStorage.getItem(key);

      return saved !== null
        ? JSON.parse(saved)
        : initialValue;
    } catch (error) {
      console.error("저장 데이터 읽기 실패:", error);
      return initialValue;
    }
  });

  // 값이 바뀌면 브라우저 저장소에도 반영합니다.
  useEffect(() => {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (error) {
      console.error("데이터 저장 실패:", error);
    }
  }, [key, value]);

  return [value, setValue];
}
```

일반적인 `useState`처럼 사용하면서 **브라우저 저장 기능을 함께 제공**합니다.

```javascript
const [todos, setTodos] = useLocalStorage("todo-app-items", []);
```

- 첫 실행: 저장된 데이터가 없으므로 `[]` 사용
- 데이터 변경: `localStorage`에 JSON 문자열로 저장
- 새로고침: 저장된 JSON을 읽어 상태 복원

이 예제는 브라우저 전용이며, 여러 탭 사이의 실시간 동기화는 포함하지 않습니다.

**② `useTodos` — 할 일 관리 로직을 묶기**

`src/hooks/useTodos.js`

```javascript
import useLocalStorage from "./useLocalStorage";

export default function useTodos() {
  const [todos, setTodos] = useLocalStorage("todo-app-items", []);

  // 할 일 추가: 공백만 입력하거나 100자를 초과하면 거절
  function addTodo(title) {
    const trimmedTitle = title.trim();

    if (!trimmedTitle || trimmedTitle.length > 100) {
      return false;
    }

    // ID 생성은 상태 업데이트 함수 밖에서 수행합니다.
    const newTodo = {
      id: crypto.randomUUID(),
      title: trimmedTitle,
      done: false,
    };

    // 최신 항목을 앞에 추가합니다.
    setTodos(prev => [newTodo, ...prev]);

    return true;
  }

  // 완료 ↔ 미완료 전환
  function toggleTodo(id) {
    setTodos(prev =>
      prev.map(todo =>
        todo.id === id
          ? { ...todo, done: !todo.done }
          : todo
      )
    );
  }

  // 할 일 삭제
  function deleteTodo(id) {
    setTodos(prev => prev.filter(todo => todo.id !== id));
  }

  // 기존 상태로 계산할 수 있으므로 별도의 state는 불필요합니다.
  const remainingCount = todos.filter(todo => !todo.done).length;

  return {
    todos,
    addTodo,
    toggleTodo,
    deleteTodo,
    remainingCount,
  };
}
```

컴포넌트는 배열을 수정하는 방법을 몰라도 아래 함수만 호출하면 됩니다.

```javascript
const { todos, addTodo, toggleTodo, deleteTodo } = useTodos();

addTodo("React 공부하기");
toggleTodo(id);
deleteTodo(id);
```

**커스텀 훅 안에서 다른 커스텀 훅을 호출할 수 있다**는 점도 이 예제의 핵심입니다.

**③ `useTodoFilter` — 화면에 표시할 항목 선택**

`src/hooks/useTodoFilter.js`

```javascript
import { useState } from "react";

export default function useTodoFilter(todos) {
  const [filter, setFilter] = useState("all");

  // 원본 todos를 수정하지 않고 표시할 목록만 계산합니다.
  const filteredTodos = todos.filter(todo => {
    if (filter === "active") {
      return !todo.done;
    }

    if (filter === "completed") {
      return todo.done;
    }

    return true;
  });

  return {
    filter,
    setFilter,
    filteredTodos,
  };
}
```

| `filter` 값 | 표시할 항목 |
|---|---|
| `"all"` | 전체 |
| `"active"` | 미완료 |
| `"completed"` | 완료 |

`filteredTodos`는 `todos`와 `filter`로 계산할 수 있으므로 **별도의 상태나 `useEffect` 없이 렌더링할 때 계산**합니다.

**세 가지 훅을 연결한 화면**

`src/App.jsx`

```jsx
import { useState } from "react";
import useTodos from "./hooks/useTodos";
import useTodoFilter from "./hooks/useTodoFilter";

export default function App() {
  const [title, setTitle] = useState("");

  // 데이터와 관리 함수 준비
  const {
    todos,
    addTodo,
    toggleTodo,
    deleteTodo,
    remainingCount,
  } = useTodos();

  // 화면에 보여 줄 목록 준비
  const {
    filter,
    setFilter,
    filteredTodos,
  } = useTodoFilter(todos);

  function handleSubmit(event) {
    event.preventDefault();

    const success = addTodo(title);

    if (success) {
      setTitle("");
    }
  }

  return (
    <main>
      <h1>Todo 앱</h1>

      <form onSubmit={handleSubmit}>
        <input
          aria-label="새 할 일"
          value={title}
          onChange={event => setTitle(event.target.value)}
          placeholder="할 일을 입력하세요"
          maxLength={100}
          required
        />
        <button type="submit" disabled={!title.trim()}>
          추가
        </button>
      </form>

      <p>
        전체 {todos.length}개 / 미완료 {remainingCount}개
      </p>

      <label>
        표시할 항목:{" "}
        <select
          value={filter}
          onChange={event => setFilter(event.target.value)}
        >
          <option value="all">전체</option>
          <option value="active">미완료</option>
          <option value="completed">완료</option>
        </select>
      </label>

      <ul>
        {filteredTodos.map(todo => (
          <li key={todo.id}>
            <label>
              <input
                type="checkbox"
                checked={todo.done}
                onChange={() => toggleTodo(todo.id)}
              />

              <span
                style={{
                  textDecoration: todo.done ? "line-through" : "none",
                }}
              >
                {todo.title}
              </span>
            </label>

            <button
              type="button"
              onClick={() => deleteTodo(todo.id)}
            >
              삭제
            </button>
          </li>
        ))}
      </ul>

      {filteredTodos.length === 0 && (
        <p>표시할 할 일이 없습니다.</p>
      )}
    </main>
  );
}
```

학습할 때 주의할 점은 **커스텀 훅이 공유하는 것은 로직이며, 상태 자체는 아니라는 것**입니다. 여러 컴포넌트에서 `useTodos()`를 각각 호출하면 각자의 상태가 생깁니다. 이 예제처럼 `App`에서 한 번 호출하고, 화면을 여러 컴포넌트로 나눌 때는 데이터와 함수를 props로 전달하세요. [React](https://react.dev/learn/reusing-logic-with-custom-hooks?utm_source=chatgpt.com)
