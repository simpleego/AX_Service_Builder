import { useState, useEffect, useRef } from 'react';

function ChatRoom({ roomId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [status, setStatus] = useState('연결 중...');
  const socketRef = useRef(null);

  useEffect(() => {
    setMessages([]); // 방을 바꾸면 이전 메시지를 지웁니다
    const socket = new WebSocket('wss://echo.websocket.org'); // 실제 테스트용 에코 서버
    socketRef.current = socket;

    socket.onopen = () => setStatus(`${roomId}번 방 연결됨`);
    socket.onmessage = (e) => setMessages(prev => [...prev, e.data]);
    socket.onerror = () => setStatus('연결 실패');
    socket.onclose = () => setStatus('연결 종료');

    return () => {
      // 아직 연결 중이면, 연결된 직후에 닫습니다 (StrictMode 경고 방지)
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
    <div>
      <p>{status}</p>
      <input value={input} onChange={e => setInput(e.target.value)} />
      <button onClick={send}>보내기</button>
      <ul>{messages.map((m, i) => <li key={i}>{m}</li>)}</ul>
    </div>
  );
}

export default ChatRoom;