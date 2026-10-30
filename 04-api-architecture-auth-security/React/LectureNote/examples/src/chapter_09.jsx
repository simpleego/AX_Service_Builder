import React, { useState } from 'react';

function Toolbar({ user, onLogin, onLogout }) {
  return <div>{user && <p>{user.name}님, 환영합니다!</p>}
    {user ? <button onClick={onLogout}>로그아웃</button> : <button onClick={onLogin}>체험 로그인</button>}
  </div>;
}
export default function LoginPractice() {
  const [user, setUser] = useState(null);
  return <section><Toolbar user={user} onLogin={() => setUser({ id: 1, name: '학습자' })} onLogout={() => setUser(null)} />
    {user ? <p>회원용 학습 화면</p> : <p>로그인하면 학습 화면을 볼 수 있습니다.</p>}
    <small>상태 전환 데모입니다. 서버 인증 기능은 포함하지 않습니다.</small>
  </section>;
}
