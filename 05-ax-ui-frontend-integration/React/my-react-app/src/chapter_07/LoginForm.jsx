import { useReducer } from "react";

const initialState = {
  email: "",
  password: "",
  showPassword: false,
};

function reducer(state, action) {
  switch (action.type) {
    case "CHANGE":
      return {
        ...state,
        [action.field]: action.value,
      };

    case "TOGGLE_PASSWORD":
      return {
        ...state,
        showPassword: !state.showPassword,
      };

    case "RESET":
      return initialState;

    default:
      return state;
  }
}

export default function LoginForm() {
  const [form, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <h2>로그인 폼</h2>

      <input
        type="email"
        placeholder="이메일"
        value={form.email}
        onChange={(e) =>
          dispatch({
            type: "CHANGE",
            field: "email",
            value: e.target.value,
          })
        }
      />

      <input
        type={form.showPassword ? "text" : "password"}
        placeholder="비밀번호"
        value={form.password}
        onChange={(e) =>
          dispatch({
            type: "CHANGE",
            field: "password",
            value: e.target.value,
          })
        }
      />

      <button onClick={() => dispatch({ type: "TOGGLE_PASSWORD" })}>
        비밀번호 표시/숨기기
      </button>

      <button onClick={() => dispatch({ type: "RESET" })}>
        초기화
      </button>

      <p>입력한 이메일: {form.email}</p>
    </div>
  );
}

