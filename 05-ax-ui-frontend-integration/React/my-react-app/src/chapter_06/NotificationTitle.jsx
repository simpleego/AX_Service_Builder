import { useState, useEffect } from 'react';

function NotificationTitle() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    console.log('컴포넌트 생성됨')
    document.title = count > 0 ? `(${count}) 새 알림` : '알림 없음';
  }, [count]); // count가 바뀔 때만 실행합니다

  return <button onClick={() => setCount(c => c + 1)}>알림 추가</button>;
}


export default NotificationTitle;