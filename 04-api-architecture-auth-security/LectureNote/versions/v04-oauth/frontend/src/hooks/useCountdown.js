import { useEffect, useState } from 'react';

/**
 * 목표 시각까지 남은 초를 1초마다 갱신하는 커스텀 Hook.
 * - useEffect + setInterval, cleanup에서 clearInterval (타이머 누수 방지)
 */
export function useCountdown(targetTime) {
  const [now, setNow] = useState(() => Date.now());

  useEffect(() => {
    if (!targetTime) return undefined;
    const timer = setInterval(() => setNow(Date.now()), 1000);
    return () => clearInterval(timer);
  }, [targetTime]);

  if (!targetTime) return null;
  return Math.max(0, Math.round((targetTime - now) / 1000));
}
