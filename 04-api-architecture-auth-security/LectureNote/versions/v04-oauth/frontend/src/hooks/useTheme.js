import { useContext } from 'react';
import { ThemeContext } from '../context/ThemeContext';

export function useTheme() {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme은 <ThemeProvider> 안에서만 사용할 수 있습니다.');
  return context;
}
