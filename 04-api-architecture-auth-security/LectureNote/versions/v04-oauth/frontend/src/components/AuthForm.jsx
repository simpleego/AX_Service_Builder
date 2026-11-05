import { useEffect, useId, useRef, useState } from 'react';

/**
 * 로그인/회원가입 공용 폼 (제어 컴포넌트)
 * - useState: 입력값, 제출 중 여부
 * - useRef + useEffect: 화면이 열리면 이메일 입력칸에 자동 포커스
 * - useId: label과 input을 연결하는 고유 id 생성 (같은 컴포넌트를 여러 번 써도 충돌 없음)
 */
export default function AuthForm({ submitLabel, onSubmit, minPasswordLength = 1, serverError, fieldErrors = {} }) {
  const [form, setForm] = useState({ email: '', password: '' });
  const [submitting, setSubmitting] = useState(false);
  const emailRef = useRef(null);
  const id = useId();

  useEffect(() => {
    emailRef.current?.focus();
  }, []);

  const handleChange = (event) => {
    const { name, value } = event.target;
    setForm((prev) => ({ ...prev, [name]: value })); // 이전 상태 기반 업데이트
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setSubmitting(true);
    try {
      await onSubmit(form.email.trim(), form.password);
    } finally {
      setSubmitting(false);
    }
  };

  const tooShort = form.password.length > 0 && form.password.length < minPasswordLength;

  return (
    <form className="form" onSubmit={handleSubmit} noValidate>
      <label htmlFor={`${id}-email`}>이메일</label>
      <input
        ref={emailRef}
        id={`${id}-email`}
        name="email"
        type="email"
        autoComplete="email"
        value={form.email}
        onChange={handleChange}
        required
      />
      {fieldErrors.email && <p className="field-error">{fieldErrors.email}</p>}

      <label htmlFor={`${id}-password`}>비밀번호</label>
      <input
        id={`${id}-password`}
        name="password"
        type="password"
        autoComplete={minPasswordLength > 1 ? 'new-password' : 'current-password'}
        value={form.password}
        onChange={handleChange}
        required
      />
      {minPasswordLength > 1 && (
        <p className={tooShort ? 'field-error' : 'hint'}>
          {minPasswordLength}자 이상 ({form.password.length}/{minPasswordLength})
        </p>
      )}
      {fieldErrors.password && <p className="field-error">{fieldErrors.password}</p>}

      {serverError && <p className="form-error">{serverError}</p>}

      <button className="btn primary" type="submit" disabled={submitting || !form.email || tooShort}>
        {submitting ? '처리 중…' : submitLabel}
      </button>
    </form>
  );
}
