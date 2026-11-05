import { useState } from 'react'

// 회원가입과 로그인을 한 화면에서 처리한다.
export default function AuthForm({ onRegister, onLogin }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')

  const handleLogin = async (e) => {
    e.preventDefault()
    setMessage('')
    try {
      await onLogin(email, password)
    } catch (error) {
      setMessage(`로그인 실패: ${error.message}`)
    }
  }

  const handleRegister = async () => {
    setMessage('')
    try {
      await onRegister(email, password)
      setMessage('가입 완료! 이제 로그인하세요.')
    } catch (error) {
      setMessage(`가입 실패: ${error.message}`)
    }
  }

  return (
    <form className="card" onSubmit={handleLogin}>
      <h2>로그인</h2>
      <input
        type="email"
        placeholder="이메일"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="비밀번호 (12자 이상)"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        minLength={12}
        required
      />
      <div className="row">
        <button type="submit">로그인</button>
        <button type="button" className="secondary" onClick={handleRegister}>
          회원가입
        </button>
      </div>
      {message && <p className="message">{message}</p>}
    </form>
  )
}
