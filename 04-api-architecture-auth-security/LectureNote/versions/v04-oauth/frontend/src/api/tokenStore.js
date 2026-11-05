// 토큰 저장소 (React 바깥의 "외부 스토어")
// - accessToken: 메모리에만 보관 (새로고침하면 사라짐 → refresh로 다시 받음)
// - refreshToken: localStorage에 보관 (새로고침 후 로그인 유지용)
//   ※ 수업용 단순화입니다. 실제 서비스는 XSS에 대비해 HttpOnly 쿠키/BFF 방식을 권장합니다.
// React 컴포넌트는 useSyncExternalStore(subscribe, getSnapshot)로 이 값을 구독합니다.

const REFRESH_KEY = 'socialAuth.refreshToken';

function readRefresh() {
  try {
    return localStorage.getItem(REFRESH_KEY);
  } catch {
    return null;
  }
}

function writeRefresh(value) {
  try {
    if (value) localStorage.setItem(REFRESH_KEY, value);
    else localStorage.removeItem(REFRESH_KEY);
  } catch {
    /* 저장소를 쓸 수 없는 환경이면 새로고침 시 로그아웃될 뿐이다. */
  }
}

// useSyncExternalStore는 값이 바뀔 때만 새 객체를 돌려줘야 하므로 snapshot을 통째로 교체한다.
let snapshot = { accessToken: null, expiresAt: null, hasRefresh: Boolean(readRefresh()) };
const listeners = new Set();

function emit(next) {
  snapshot = next;
  listeners.forEach((listener) => listener());
}

export const tokenStore = {
  subscribe(listener) {
    listeners.add(listener);
    return () => listeners.delete(listener);
  },
  getSnapshot() {
    return snapshot;
  },
  getAccessToken() {
    return snapshot.accessToken;
  },
  getRefreshToken() {
    return readRefresh();
  },
  /** 로그인/갱신 응답(TokenPair)을 저장한다. */
  set({ accessToken, refreshToken, expiresIn }) {
    writeRefresh(refreshToken);
    emit({ accessToken, expiresAt: Date.now() + expiresIn * 1000, hasRefresh: true });
  },
  clear() {
    writeRefresh(null);
    emit({ accessToken: null, expiresAt: null, hasRefresh: false });
  },
};
