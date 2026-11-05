import { Navigate, Outlet, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

function FullPageSpinner() {
  return (
    <div className="center-box">
      <div className="spinner" aria-label="불러오는 중" />
    </div>
  );
}

/** 로그인한 사용자만 통과. 아니면 /login으로 보내고, 원래 가려던 주소를 기억한다. */
export function ProtectedRoute() {
  const { status } = useAuth();
  const location = useLocation();
  if (status === 'loading') return <FullPageSpinner />;
  if (status !== 'authenticated') return <Navigate to="/login" replace state={{ from: location }} />;
  return <Outlet />;
}

/** 로그인/회원가입 화면은 이미 로그인했으면 보여줄 필요가 없다. */
export function PublicOnlyRoute() {
  const { status } = useAuth();
  const location = useLocation();
  if (status === 'loading') return <FullPageSpinner />;
  if (status === 'authenticated') return <Navigate to={location.state?.from?.pathname || '/'} replace />;
  return <Outlet />;
}
