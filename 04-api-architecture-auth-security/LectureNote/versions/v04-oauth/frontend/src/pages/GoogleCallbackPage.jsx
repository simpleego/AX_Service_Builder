import { useEffect, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../hooks/useToast';
import { messageOf } from '../api/messages';

/**
 * Google 로그인 후 백엔드가 보내주는 화면: /auth/callback?code=일회용코드 (또는 ?error=코드)
 *
 * - useSearchParams: 주소의 code/error 읽기
 * - useRef: 일회용 코드를 "딱 한 번만" 교환하기 위한 플래그
 *   개발 모드의 StrictMode는 effect를 두 번 실행하는데, 같은 코드를 두 번 보내면
 *   두 번째는 서버에서 INVALID_HANDOFF가 된다. ref는 다시 렌더링해도 값이 유지되므로 중복 실행을 막는다.
 */
export default function GoogleCallbackPage() {
  const [params] = useSearchParams();
  const navigate = useNavigate();
  const { completeGoogleLogin } = useAuth();
  const { showToast } = useToast();
  const [error, setError] = useState('');
  const started = useRef(false);

  useEffect(() => {
    if (started.current) return;
    started.current = true;

    const code = params.get('code');
    const errorCode = params.get('error');
    if (errorCode || !code) {
      setError(messageOf({ code: errorCode || 'INVALID_HANDOFF' }));
      return;
    }
    completeGoogleLogin(code)
      .then((user) => {
        const email = user.identities.find((i) => i.provider === 'google')?.email;
        showToast(`Google 계정${email ? `(${email})` : ''}으로 로그인했습니다.`, 'success');
        navigate('/', { replace: true }); // replace: 뒤로가기로 일회용 코드 주소에 돌아오지 않게
      })
      .catch((err) => setError(messageOf(err)));
  }, [params, completeGoogleLogin, navigate, showToast]);

  return (
    <section className="card auth-card center">
      {error ? (
        <>
          <h1>로그인 실패</h1>
          <p className="form-error">{error}</p>
          <Link className="btn primary" to="/login" replace>
            로그인 화면으로
          </Link>
        </>
      ) : (
        <>
          <div className="spinner" />
          <p>Google 로그인 처리 중…</p>
        </>
      )}
    </section>
  );
}
