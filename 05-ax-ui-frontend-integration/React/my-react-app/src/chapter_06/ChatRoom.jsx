import { useState, useEffect, useRef } from 'react';

function ChatRoom({ roomId, onLeave }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [status, setStatus] = useState('연결 중...');
  const socketRef = useRef(null);

  useEffect(() => {
    setMessages([]);
    const socket = new WebSocket('wss://echo.websocket.org');
    socketRef.current = socket;

    socket.onopen = () => setStatus(`${roomId}번 방 연결됨`);
    socket.onmessage = (e) => setMessages(prev => [...prev, e.data]);
    socket.onerror = () => setStatus('연결 실패');
    socket.onclose = () => setStatus('연결 종료');

    // 방을 나가면(컴포넌트가 사라지면) 여기서 연결을 닫습니다
    return () => {
      console.log(`${roomId}번 방 연결 종료`);
      if (socket.readyState === WebSocket.CONNECTING) {
        socket.onopen = () => socket.close();
      } else {
        socket.close();
      }
    };
  }, [roomId]);

  const send = () => {
    if (socketRef.current?.readyState === WebSocket.OPEN && input) {
      socketRef.current.send(`[${roomId}번 방] ${input}`);
      setInput('');
    }
  };

  return (
    <div style={{ border: '1px solid #ccc', padding: 12, marginBottom: 12 }}>
      <h3>
        {roomId}번 방 <button onClick={() => onLeave(roomId)}>나가기</button>
      </h3>
      <p>{status}</p>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        onKeyDown={e => e.key === 'Enter' && send()}
      />
      <button onClick={send}>보내기</button>
      <ul>{messages.map((m, i) => <li key={i}>{m}</li>)}</ul>
    </div>
  );
}

export default ChatRoom;