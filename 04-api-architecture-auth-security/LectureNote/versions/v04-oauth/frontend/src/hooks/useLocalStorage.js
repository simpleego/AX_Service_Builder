import { useCallback, useState } from 'react';

/**
 * useState와 같지만 값을 localStorage에도 저장하는 커스텀 Hook.
 * - useState의 "지연 초기화"(함수 전달)로 최초 렌더링 때만 localStorage를 읽는다.
 */
export function useLocalStorage(key, initialValue) {
  const [value, setValue] = useState(() => {
    try {
      const saved = localStorage.getItem(key);
      return saved !== null ? JSON.parse(saved) : initialValue;
    } catch {
      return initialValue;
    }
  });

  const setStoredValue = useCallback(
    (next) => {
      setValue((prev) => {
        const resolved = typeof next === 'function' ? next(prev) : next;
        try {
          localStorage.setItem(key, JSON.stringify(resolved));
        } catch {
          /* 저장 실패해도 화면 상태는 유지 */
        }
        return resolved;
      });
    },
    [key],
  );

  return [value, setStoredValue];
}
