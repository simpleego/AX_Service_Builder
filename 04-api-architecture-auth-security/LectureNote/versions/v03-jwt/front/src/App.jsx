import { useState } from 'react'
import { useAuth } from './useAuth'
import AuthForm from './AuthForm'
import TodoPanel from './TodoPanel'

// 라우터 없이 로그인 여부에 따라 화면 하나만 바꿔 보여 준다.
export default function App() {
  const auth = useAuth()
  const [notice, setNotice] = useState('')

  // 실습용: access 토큰을 수동으로 갱신해 refresh 회전을 확인한다.
  const handleRefresh = async () => {
    try {
      await auth.refresh()
      setNotice('토큰을 갱신했습니다. (refresh 회전)')
    } catch (error) {
      setNotice(`갱신 실패: ${error.message}`)
    }
  }

  return (
    <main>
      <header>
        <h1>Todo · JWT 실습</h1>
        {auth.isLoggedIn && (
          <div className="row">
            <span>{auth.email}</span>
            <button className="secondary" onClick={handleRefresh}>
              토큰 갱신
            </button>
            <button className="secondary" onClick={auth.logout}>
              로그아웃
            </button>
          </div>
        )}
      </header>

      {notice && auth.isLoggedIn && <p className="notice">{notice}</p>}

      {auth.isLoggedIn ? (
        <TodoPanel authRequest={auth.authRequest} />
      ) : (
        <AuthForm onRegister={auth.register} onLogin={auth.login} />
      )}
    </main>
  )
}
