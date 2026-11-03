import { useState, useEffect } from 'react';

function Clock() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    console.log('called!!')
    return () => clearInterval(id); // 정리하지 않으면 타이머가 계속 쌓입니다
  }, []);

  return <p>현재 시각: {now.toLocaleTimeString()}</p>;
}

export default Clock;