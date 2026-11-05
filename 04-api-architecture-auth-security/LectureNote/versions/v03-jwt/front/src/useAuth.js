import { useCallback, useRef, useState } from 'react'
import { request } from './api'

// 로그인 상태와 토큰을 관리하는 Hook.
// 토큰은 메모리(state)에만 둔다. 새로고침하면 로그아웃되지만 localStorage 탈취 위험이 없다.
export function useAuth() {
  const [email, setEmail] = useState(null)
  const [tokens, setTokens] = useState(null)
  // 비동기 함수 안에서 항상 최신 토큰을 읽기 위해 ref에도 보관한다.
  const tokensRef = useRef(null)
  // 동시에 여러 요청이 401을 받아도 refresh는 한 번만 보낸다.
  // 같은 refresh 토큰을 두 번 보내면 서버가 재사용 공격으로 보고 세션 전체를 폐기하기 때문이다.
  const refreshingRef = useRef(null)

  const saveTokens = useCallback((next) => {
    tokensRef.current = next
    setTokens(next)
  }, [])

  const clear = useCallback(() => {
    saveTokens(null)
    setEmail(null)
  }, [saveTokens])

  const register = useCallback(
    (userEmail, password) =>
      request('/api/auth/register', { method: 'POST', body: { email: userEmail, password } }),
    [],
  )

  const login = useCallback(
    async (userEmail, password) => {
      const pair = await request('/api/auth/login', {
        method: 'POST',
        body: { email: userEmail, password },
      })
      saveTokens(pair)
      setEmail(userEmail)
    },
    [saveTokens],
  )

  const refresh = useCallback(() => {
    if (!refreshingRef.current) {
      refreshingRef.current = request('/api/auth/refresh', {
        method: 'POST',
        body: { refreshToken: tokensRef.current?.refreshToken },
      })
        .then((pair) => {
          saveTokens(pair)
          return pair
        })
        .finally(() => {
          refreshingRef.current = null
        })
    }
    return refreshingRef.current
  }, [saveTokens])

  const logout = useCallback(async () => {
    const refreshToken = tokensRef.current?.refreshToken
    clear()
    if (refreshToken) {
      await request('/api/auth/logout', { method: 'POST', body: { refreshToken } }).catch(() => {})
    }
  }, [clear])

  // 인증이 필요한 요청. access가 만료되어 401이면 refresh 후 한 번만 다시 시도한다.
  const authRequest = useCallback(
    async (path, options = {}) => {
      try {
        return await request(path, { ...options, token: tokensRef.current?.accessToken })
      } catch (error) {
        if (error.status !== 401 || !tokensRef.current) throw error
        try {
          const pair = await refresh()
          return await request(path, { ...options, token: pair.accessToken })
        } catch (refreshError) {
          clear() // refresh까지 실패하면 다시 로그인해야 한다.
          throw refreshError
        }
      }
    },
    [refresh, clear],
  )

  return { email, tokens, isLoggedIn: tokens !== null, register, login, logout, refresh, authRequest }
}
