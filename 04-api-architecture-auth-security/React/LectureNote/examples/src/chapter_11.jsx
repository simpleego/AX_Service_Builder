import React, { useState } from 'react';
export default function SignUpPractice() {
  const [name, setName] = useState('');
  const [course, setCourse] = useState('react');
  const [agreed, setAgreed] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  function submit(event) {
    event.preventDefault();
    setResult(null);
    if (!name.trim()) { setError('이름을 입력하세요.'); return; }
    if (!agreed) { setError('실습 안내 확인에 체크하세요.'); return; }
    setError('');
    setResult({ name: name.trim(), course });
  }
  return <form onSubmit={submit} noValidate>
    <label>이름 <input value={name} onChange={event => setName(event.target.value)} aria-describedby={error ? 'form-error' : undefined} /></label>
    <label>과정 <select value={course} onChange={event => setCourse(event.target.value)}><option value="react">React</option><option value="javascript">JavaScript</option></select></label>
    <label><input type="checkbox" checked={agreed} onChange={event => setAgreed(event.target.checked)} />실습 안내를 확인했습니다.</label>
    <button type="submit">등록 미리보기</button>
    {error && <p id="form-error" role="alert">{error}</p>}
    {result && <p role="status">{result.name} / {result.course} 등록 정보를 확인했습니다.</p>}
  </form>;
}
