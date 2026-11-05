import { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';

/** useContext를 감싼 커스텀 Hook. Provider 밖에서 쓰면 바로 알 수 있게 오류를 던진다. */
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth는 <AuthProvider> 안에서만 사용할 수 있습니다.');
  return context;
}
