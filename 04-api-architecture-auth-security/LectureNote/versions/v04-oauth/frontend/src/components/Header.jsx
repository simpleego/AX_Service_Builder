import { Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { useTheme } from '../hooks/useTheme';

/** 여러 Context를 동시에 사용하는 예: 로그인 정보(AuthContext) + 테마(ThemeContext) */
export default function Header() {
  const { isAuthenticated, user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const displayEmail = user?.email || user?.identities?.[0]?.email || `사용자 #${user?.id}`;

  return (
    <header className="header">
      <Link to="/" className="brand">
        ✓ Social Auth Todo
      </Link>
      <div className="header-right">
        <button className="btn ghost icon" onClick={toggleTheme} aria-label="테마 전환" title="테마 전환">
          {theme === 'dark' ? '☀' : '☾'}
        </button>
        {isAuthenticated && (
          <>
            <span className="header-user">{displayEmail}</span>
            <button className="btn ghost" onClick={logout}>
              로그아웃
            </button>
          </>
        )}
      </div>
    </header>
  );
}
