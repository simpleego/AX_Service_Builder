import React, { createContext, useContext, useState } from 'react';
const ThemeContext = createContext(null);
function useTheme() {
  const value = useContext(ThemeContext);
  if (value === null) throw new Error('ThemeProvider 내부에서 사용하세요.');
  return value;
}
function ThemeProvider({ children }) {
  const [theme, setTheme] = useState('light');
  const toggleTheme = () => setTheme(previous => previous === 'light' ? 'dark' : 'light');
  return <ThemeContext.Provider value={{ theme, toggleTheme }}>{children}</ThemeContext.Provider>;
}
function ThemeButton() {
  const { theme, toggleTheme } = useTheme();
  return <button onClick={toggleTheme}>현재 {theme} / 테마 변경</button>;
}
function Layout({ children }) { return <div className="card">{children}</div>; }
function MainContent() {
  const { theme } = useTheme();
  return <section style={{ padding: 24, backgroundColor: theme === 'light' ? '#fff' : '#222', color: theme === 'light' ? '#222' : '#fff' }}>
    <p>Layout은 테마 props를 전달하지 않습니다.</p><Layout><ThemeButton /></Layout>
  </section>;
}
export default function ContextPractice() {
  return <ThemeProvider><MainContent /></ThemeProvider>;
}
