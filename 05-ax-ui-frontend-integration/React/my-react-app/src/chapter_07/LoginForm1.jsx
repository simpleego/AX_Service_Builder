import { useRef, useEffect } from 'react';

function LoginForm() {
  const idRef = useRef(null);

  useEffect(() => {
    idRef.current.focus(); // 처음 렌더링되면 아이디 입력창에 포커스
  }, []);

  return (
    <form>
      <input ref={idRef} placeholder="아이디" />
      <input type="password" placeholder="비밀번호" />
      <button type="button" onClick={() => idRef.current.focus()}>
        아이디 다시 입력
      </button>
    </form>
  );
}

export default LoginForm;