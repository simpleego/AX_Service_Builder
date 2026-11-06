import { useReducer, useState } from "react";

const initialTodos = [
  { id: 1, text: "React 공부", done: false },
  { id: 2, text: "useReducer 실습", done: true },
];

function reducer(state, action) {
  switch (action.type) {
    case "ADD":
      return [
        ...state,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];

    case "TOGGLE":
      return state.map((todo) =>
        todo.id === action.id
          ? { ...todo, done: !todo.done }
          : todo
      );

    case "DELETE":
      return state.filter((todo) => todo.id !== action.id);

    case "CLEAR_COMPLETED":
      return state.filter((todo) => !todo.done);

    default:
      return state;
  }
}

export default function TodoApp() {
  const [todos, dispatch] = useReducer(reducer, initialTodos);
  const [text, setText] = useState("");

  function handleAdd() {
    const value = text.trim();
    if (!value) return;

    dispatch({
      type: "ADD",
      id: crypto.randomUUID(),
      text: value,
    });

    setText("");
  }

  return (
    <div>
      <h2>Todo 앱</h2>

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="할 일 입력"
      />

      <button onClick={handleAdd}>추가</button>

      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() =>
                dispatch({ type: "TOGGLE", id: todo.id })
              }
            />

            <span
              style={{
                textDecoration: todo.done ? "line-through" : "none",
              }}
            >
              {todo.text}
            </span>

            <button
              onClick={() =>
                dispatch({ type: "DELETE", id: todo.id })
              }
            >
              삭제
            </button>
          </li>
        ))}
      </ul>

      <button onClick={() => dispatch({ type: "CLEAR_COMPLETED" })}>
        완료 항목 삭제
      </button>

      <p>전체: {todos.length}개</p>
    </div>
  );
}