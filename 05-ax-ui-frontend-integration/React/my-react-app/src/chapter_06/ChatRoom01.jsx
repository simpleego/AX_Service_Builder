import { useState, useEffect } from 'react';

function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const socket = new WebSocket(`wss://example.com/chat/${roomId}`);
    socket.onmessage = (e) => setMessages(prev => [...prev, e.data]);

    return () => socket.close(); // 방을 바꾸면 이전 방 연결을 닫습니다
  }, [roomId]);

  return <ul>{messages.map((m, i) => <li key={i}>{m}</li>)}</ul>;
}

export default ChatRoom;