import { useMemo, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../hooks/useToast';
import { useCountdown } from '../hooks/useCountdown';
import { messageOf } from '../api/messages';

function decodeJwt(token) {
  try {
    const base64 = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    return JSON.parse(atob(base64));
  } catch {
    return null;
  }
}

function formatSeconds(total) {
  const m = Math.floor(total / 60);
  const s = String(total % 60).padStart(2, '0');
  return `${m}:${s}`;
}

/**
 * 로그인 세션 정보 (학습용 패널)
 * - useCountdown (커스텀 Hook): access 토큰 남은 시간을 1초마다 표시
 * - useMemo: 토큰이 바뀔 때만 JWT payload를 다시 디코딩
 * - Context 값(accessToken, expiresAt)은 자동 refresh가 일어나도 즉시 갱신된다.
 */
export default function SessionPanel() {
  const { user, accessToken, expiresAt, refreshNow } = useAuth();
  const { showToast } = useToast();
  const [showPayload, setShowPayload] = useState(false);
  const remaining = useCountdown(expiresAt);
  const payload = useMemo(() => (accessToken ? decodeJwt(accessToken) : null), [accessToken]);

  const handleRefresh = async () => {
    try {
      await refreshNow();
      showToast('토큰을 새로 발급받았습니다.', 'success');
    } catch (error) {
      showToast(messageOf(error), 'error');
    }
  };

  if (!user) return null;
  const google = user.identities.find((i) => i.provider === 'google');

  return (
    <aside className="card session">
      <h2>내 세션</h2>
      <dl>
        <dt>회원 번호</dt>
        <dd>#{user.id}</dd>
        <dt>가입 방식</dt>
        <dd>
          {user.hasPassword && <span className="badge">이메일</span>}
          {google && <span className="badge google">Google</span>}
        </dd>
        <dt>이메일</dt>
        <dd className="break">{user.email || google?.email || '없음'}</dd>
        <dt>Access 토큰</dt>
        <dd>
          {remaining === null ? (
            '-'
          ) : (
            <span className={remaining < 60 ? 'warn' : ''}>{formatSeconds(remaining)} 남음</span>
          )}
        </dd>
      </dl>
      <p className="hint small">
        만료되면 다음 요청 때 refresh 토큰으로 자동 재발급됩니다. 새로고침해도 로그인이 유지됩니다.
      </p>
      <div className="session-actions">
        <button className="btn" onClick={handleRefresh}>
          토큰 지금 갱신
        </button>
        <button className="btn ghost" onClick={() => setShowPayload((v) => !v)}>
          {showPayload ? 'JWT 숨기기' : 'JWT 내용 보기'}
        </button>
      </div>
      {showPayload && payload && <pre className="payload">{JSON.stringify(payload, null, 2)}</pre>}
    </aside>
  );
}
