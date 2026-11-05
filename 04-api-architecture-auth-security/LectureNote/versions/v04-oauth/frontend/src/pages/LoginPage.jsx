import { useState } from 'react';
import { Link } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import GoogleButton from '../components/GoogleButton';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../hooks/useToast';
import { fieldErrorsOf, messageOf } from '../api/messages';

export default function LoginPage() {
  const { login } = useAuth();
  const { showToast } = useToast();
  const [error, setError] = useState({ message: '', fields: {} });

  // 로그인에 성공하면 AuthContext 상태가 바뀌고, PublicOnlyRoute가 자동으로 원래 화면으로 보낸다.
  const handleLogin = async (email, password) => {
    setError({ message: '', fields: {} });
    try {
      const user = await login(email, password);
      showToast(`${user.email}님 환영합니다.`, 'success');
    } catch (err) {
      setError({ message: messageOf(err), fields: fieldErrorsOf(err) });
    }
  };

  return (
    <section className="card auth-card">
      <h1>로그인</h1>
      <GoogleButton />
      <div className="divider">
        <span>또는 이메일로 로그인</span>
      </div>
      <AuthForm submitLabel="로그인" onSubmit={handleLogin} serverError={error.message} fieldErrors={error.fields} />
      <p className="switch">
        계정이 없나요? <Link to="/register">회원가입</Link>
      </p>
    </section>
  );
}
