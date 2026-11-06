import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "INCREMENT":
      return state + 1;
    case "DECREMENT":
      return state - 1;
    case "RESET":
      return 0;
    default:
      return state;
  }
}

export default function Counter() {
  const [count, dispatch] = useReducer(reducer, 0);

  return (
    <div>
      <h2>카운터: {count}</h2>

      <button onClick={() => dispatch({ type: "INCREMENT" })}>
        + 증가
      </button>

      <button onClick={() => dispatch({ type: "DECREMENT" })}>
        - 감소
      </button>

      <button onClick={() => dispatch({ type: "RESET" })}>
        초기화
      </button>
    </div>
  );
}