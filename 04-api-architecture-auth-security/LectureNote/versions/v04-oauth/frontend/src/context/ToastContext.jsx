import { createContext, useCallback, useEffect, useMemo, useRef, useState } from 'react';

/**
 * ToastContext — 어느 컴포넌트에서든 알림 메시지를 띄우는 기능
 *
 * 사용 Hook
 * - useState: 화면에 떠 있는 알림 목록
 * - useRef: 알림 id 카운터와 타이머 목록 (값이 바뀌어도 다시 렌더링할 필요 없음)
 * - useCallback: showToast 참조를 고정해 이 함수를 의존성으로 쓰는 effect가 반복 실행되지 않게 함
 * - useEffect: Provider가 사라질 때 남은 타이머 정리 (cleanup)
 */
export const ToastContext = createContext(null);

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);
  const nextId = useRef(1);
  const timers = useRef(new Map());

  const dismiss = useCallback((id) => {
    setToasts((list) => list.filter((toast) => toast.id !== id));
    clearTimeout(timers.current.get(id));
    timers.current.delete(id);
  }, []);

  const showToast = useCallback(
    (message, type = 'info') => {
      const id = nextId.current++;
      setToasts((list) => [...list, { id, message, type }]);
      timers.current.set(id, setTimeout(() => dismiss(id), 3500));
    },
    [dismiss],
  );

  useEffect(() => {
    const map = timers.current;
    return () => map.forEach((timer) => clearTimeout(timer));
  }, []);

  const value = useMemo(() => ({ showToast }), [showToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        {toasts.map((toast) => (
          <button key={toast.id} className={`toast toast-${toast.type}`} onClick={() => dismiss(toast.id)}>
            {toast.message}
          </button>
        ))}
      </div>
    </ToastContext.Provider>
  );
}
