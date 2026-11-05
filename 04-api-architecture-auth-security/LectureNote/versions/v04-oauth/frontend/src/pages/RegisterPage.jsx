import { useState } from 'react';
import { Link } from 'react-router-dom';
import AuthForm from '../components/AuthForm';
import GoogleButton from '../components/GoogleButton';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../hooks/useToast';
import { fieldErrorsOf, messageOf } from '../api/messages';

export default function RegisterPage() {
  const { register } = useAuth();
  const { showToast } = useToast();
  const [error, setError] = useState({ message: '', fields: {} });

  const handleRegister = async (email, password) => {
    setError({ message: '', fields: {} });
    try {
      await register(email, password);
      showToast('회원가입이 완료되었습니다.', 'success');
    } catch (err) {
      setError({ message: messageOf(err), fields: fieldErrorsOf(err) });
    }
  };

  return (
    <section className="card auth-card">
      <h1>회원가입</h1>
      <GoogleButton label="Google 계정으로 가입하기" />
      <div className="divider">
        <span>또는 이메일로 가입</span>
      </div>
      <AuthForm
        submitLabel="가입하기"
        onSubmit={handleRegister}
        minPasswordLength={12}
        serverError={error.message}
        fieldErrors={error.fields}
      />
      <p className="hint small">
        같은 이메일이라도 Google 계정과 이메일 계정은 자동으로 합쳐지지 않고 서로 다른 회원이 됩니다.
      </p>
      <p className="switch">
        이미 계정이 있나요? <Link to="/login">로그인</Link>
      </p>
    </section>
  );
}
