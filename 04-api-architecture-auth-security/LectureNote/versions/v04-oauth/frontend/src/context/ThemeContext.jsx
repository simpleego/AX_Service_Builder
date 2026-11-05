import { createContext, useCallback, useEffect, useMemo } from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

/**
 * ThemeContext — 라이트/다크 테마를 앱 전체에 공유
 *
 * 사용 Hook
 * - useLocalStorage (커스텀 Hook): 선택한 테마를 새로고침 후에도 유지
 * - useEffect: 테마가 바뀌면 <html data-theme>에 반영 (React 바깥 DOM과 동기화)
 */
export const ThemeContext = createContext(null);

export function ThemeProvider({ children }) {
  const prefersDark = typeof window !== 'undefined' && window.matchMedia?.('(prefers-color-scheme: dark)').matches;
  const [theme, setTheme] = useLocalStorage('socialAuth.theme', prefersDark ? 'dark' : 'light');

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
  }, [theme]);

  const toggleTheme = useCallback(() => setTheme((t) => (t === 'dark' ? 'light' : 'dark')), [setTheme]);
  const value = useMemo(() => ({ theme, toggleTheme }), [theme, toggleTheme]);

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}
