import { useRef, useEffect } from 'react';

function ChatBox({ messages }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    // 메시지가 추가될 때마다 맨 아래로 스크롤합니다
    bottomRef.current.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div style={{ height: 300, overflowY: 'auto' }}>
      {messages.map((m, i) => <p key={i}>{m}</p>)}
      <div ref={bottomRef} />
    </div>
  );
}

export default ChatBox;