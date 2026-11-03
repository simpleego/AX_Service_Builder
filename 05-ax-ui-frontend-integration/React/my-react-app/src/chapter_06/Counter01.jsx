import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0); 
  // [현재값, 변경함수] = useState(초기값)

  return (
    <div>
      <p>현재 값: {count}</p>
      <button onClick={() => setCount(count + 1)}>+1</button>
      {/* 이전 값을 기준으로 바꿀 때는 함수형 업데이트가 안전합니다 */}
      <button onClick={() => setCount(prev => prev - 1)}>-1</button>
    </div>
  );
}

export default Counter; // 다른 파일에서 쓸 수 있게 내보냅니다