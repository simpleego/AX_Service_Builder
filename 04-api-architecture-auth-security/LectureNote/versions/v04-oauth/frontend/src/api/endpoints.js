import { authRequest, publicRequest } from './client';
import { tokenStore } from './tokenStore';

export const authApi = {
  register: (email, password) =>
    publicRequest('/api/auth/register', { method: 'POST', body: { email, password } }),
  login: (email, password) =>
    publicRequest('/api/auth/login', { method: 'POST', body: { email, password } }),
  logout: () => {
    const refreshToken = tokenStore.getRefreshToken();
    if (!refreshToken) return Promise.resolve();
    return publicRequest('/api/auth/logout', { method: 'POST', body: { refreshToken } });
  },
  me: () => authRequest('/api/auth/me'),
  /** Google 로그인 후 받은 60초 일회용 코드를 앱 토큰으로 교환한다. */
  exchangeGoogleCode: (code) =>
    publicRequest('/api/auth/google/exchange', { method: 'POST', body: { code } }),
  /** 브라우저 전체를 백엔드로 이동시켜 Google 로그인을 시작한다. (fetch로는 불가) */
  googleLoginUrl: '/api/auth/google?client=web',
};

export const todoApi = {
  list: ({ signal } = {}) => authRequest('/api/todos?page=1&limit=100', { signal }),
  create: (title) => authRequest('/api/todos', { method: 'POST', body: { title } }),
  update: (id, patch) => authRequest(`/api/todos/${id}`, { method: 'PATCH', body: patch }),
  remove: (id) => authRequest(`/api/todos/${id}`, { method: 'DELETE' }),
};
