import { createContext, useCallback, useEffect, useMemo, useReducer, useRef, useSyncExternalStore } from 'react';
import { authApi } from '../api/endpoints';
import { refreshTokens } from '../api/client';
import { tokenStore } from '../api/tokenStore';
import { useToast } from '../hooks/useToast';

/**
 * AuthContext — 앱 전체가 공유하는 "로그인 상태"
 *
 * 사용 Hook
 * - useReducer: 로그인 상태 전이(loading → authenticated / anonymous)를 한 곳에서 관리
 * - useSyncExternalStore: React 밖의 tokenStore(토큰)를 구독. 자동 refresh로 토큰이 바뀌면 화면도 갱신
 * - useEffect: 앱 시작 시 세션 복원, 토큰이 사라지면(세션 만료) 로그아웃 처리
 * - useCallback: Context로 내려보내는 함수의 참조를 고정 → 하위 컴포넌트 불필요한 재실행 방지
 * - useMemo: Context value 객체를 상태가 바뀔 때만 새로 만든다
 * - useRef: 렌더링과 무관한 값(직접 로그아웃했는지 여부) 보관
 */
export const AuthContext = createContext(null);

const initialState = { status: 'loading', user: null };

function authReducer(state, action) {
  switch (action.type) {
    case 'AUTHENTICATED':
      return { status: 'authenticated', user: action.user };
    case 'ANONYMOUS':
      return { status: 'anonymous', user: null };
    default:
      throw new Error(`알 수 없는 action: ${action.type}`);
  }
}

export function AuthProvider({ children }) {
  const [state, dispatch] = useReducer(authReducer, initialState);
  const session = useSyncExternalStore(tokenStore.subscribe, tokenStore.getSnapshot);
  const { showToast } = useToast();
  const manualLogout = useRef(false);

  // 토큰을 저장한 뒤 /me로 사용자 정보를 읽어 로그인 상태로 전환한다.
  const loadUser = useCallback(async () => {
    const user = await authApi.me();
    manualLogout.current = false;
    dispatch({ type: 'AUTHENTICATED', user });
    return user;
  }, []);

  // ① 앱 시작: 저장된 refresh 토큰이 있으면 새 access 토큰을 받아 로그인 상태를 복원한다.
  useEffect(() => {
    let ignore = false; // StrictMode 이중 실행/언마운트 후 setState 방지
    async function restore() {
      if (!tokenStore.getRefreshToken()) {
        dispatch({ type: 'ANONYMOUS' });
        return;
      }
      try {
        await refreshTokens(); // 동시에 여러 번 불려도 실제 요청은 1번
        const user = await authApi.me();
        if (!ignore) dispatch({ type: 'AUTHENTICATED', user });
      } catch {
        if (!ignore) dispatch({ type: 'ANONYMOUS' });
      }
    }
    restore();
    return () => {
      ignore = true;
    };
  }, []);

  // ② 로그인 중에 토큰이 사라지면(refresh 실패 = 세션 만료) 로그아웃 상태로 바꾼다.
  useEffect(() => {
    if (state.status === 'authenticated' && !session.hasRefresh) {
      dispatch({ type: 'ANONYMOUS' });
      if (!manualLogout.current) showToast('세션이 만료되어 로그아웃되었습니다.', 'error');
      manualLogout.current = false;
    }
  }, [session.hasRefresh, state.status, showToast]);

  const login = useCallback(
    async (email, password) => {
      tokenStore.set(await authApi.login(email, password));
      return loadUser();
    },
    [loadUser],
  );

  const register = useCallback(
    async (email, password) => {
      await authApi.register(email, password);
      return login(email, password); // 가입 직후 자동 로그인
    },
    [login],
  );

  const logout = useCallback(async () => {
    manualLogout.current = true;
    try {
      await authApi.logout(); // 서버에서 refresh 토큰 폐기
    } finally {
      tokenStore.clear();
      dispatch({ type: 'ANONYMOUS' });
    }
  }, []);

  const startGoogleLogin = useCallback(() => {
    // OAuth는 페이지 이동(리다이렉트)으로 진행되므로 fetch가 아니라 주소를 바꾼다.
    window.location.assign(authApi.googleLoginUrl);
  }, []);

  const completeGoogleLogin = useCallback(
    async (code) => {
      tokenStore.set(await authApi.exchangeGoogleCode(code));
      return loadUser();
    },
    [loadUser],
  );

  const refreshNow = useCallback(() => refreshTokens(), []);

  const value = useMemo(
    () => ({
      status: state.status,
      user: state.user,
      isAuthenticated: state.status === 'authenticated',
      accessToken: session.accessToken,
      expiresAt: session.expiresAt,
      login,
      register,
      logout,
      startGoogleLogin,
      completeGoogleLogin,
      refreshNow,
    }),
    [state, session, login, register, logout, startGoogleLogin, completeGoogleLogin, refreshNow],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
