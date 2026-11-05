import { tokenStore } from './tokenStore';

export class ApiError extends Error {
  constructor(status, code, fields) {
    super(code || `HTTP_${status}`);
    this.status = status;
    this.code = code || `HTTP_${status}`;
    this.fields = fields || [];
  }
}

async function parseBody(response) {
  if (response.status === 204) return null;
  const text = await response.text();
  if (!text) return null;
  try {
    return JSON.parse(text);
  } catch {
    return text;
  }
}

async function send(path, { method = 'GET', body, token, signal } = {}) {
  const headers = {};
  if (body !== undefined) headers['Content-Type'] = 'application/json';
  if (token) headers.Authorization = `Bearer ${token}`;
  const response = await fetch(path, {
    method,
    headers,
    signal, // useEffect cleanup에서 AbortController로 요청을 취소할 수 있다.
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await parseBody(response);
  if (!response.ok) {
    throw new ApiError(response.status, data?.error?.code, data?.error?.fields);
  }
  return data;
}

// ── refresh는 동시에 한 번만 ──────────────────────────────────────────
// 서버는 이미 사용한 refresh 토큰이 다시 오면 "탈취"로 보고 세션 전체를 폐기한다.
// 그래서 여러 요청이 동시에 401을 받아도 refresh 요청은 1번만 보내고 결과를 공유한다.
// (React StrictMode가 개발 중 effect를 두 번 실행해도 안전하다.)
let refreshPromise = null;

export function refreshTokens() {
  if (!refreshPromise) {
    refreshPromise = (async () => {
      const refreshToken = tokenStore.getRefreshToken();
      if (!refreshToken) throw new ApiError(401, 'NO_REFRESH_TOKEN');
      try {
        const tokens = await send('/api/auth/refresh', { method: 'POST', body: { refreshToken } });
        tokenStore.set(tokens);
        return tokens;
      } catch (error) {
        if (error.status === 401 || error.status === 422) tokenStore.clear();
        throw error;
      }
    })().finally(() => {
      refreshPromise = null;
    });
  }
  return refreshPromise;
}

/**
 * 인증이 필요한 API 호출.
 * access 토큰이 없거나 만료(401)면 refresh 후 한 번만 다시 시도한다.
 */
export async function authRequest(path, options = {}) {
  let token = tokenStore.getAccessToken();
  if (!token) token = (await refreshTokens()).accessToken;
  try {
    return await send(path, { ...options, token });
  } catch (error) {
    if (error.status !== 401) throw error;
    const tokens = await refreshTokens();
    return send(path, { ...options, token: tokens.accessToken });
  }
}

/** 인증이 필요 없는 API 호출 (회원가입, 로그인 등). */
export function publicRequest(path, options = {}) {
  return send(path, options);
}
