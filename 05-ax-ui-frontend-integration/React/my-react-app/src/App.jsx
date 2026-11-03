import { useState } from 'react';
import ChatRoom from './chapter_06/ChatRoom';

const ALL_ROOMS = [1, 2, 3];

function App() {
  const [joinedRooms, setJoinedRooms] = useState([1, 2, 3]);

  const joinRoom = (roomId) => {
    setJoinedRooms(prev => (prev.includes(roomId) ? prev : [...prev, roomId].sort()));
  };

  const leaveRoom = (roomId) => {
    setJoinedRooms(prev => prev.filter(id => id !== roomId));
  };

  return (
    <div>
      <h1>채팅방</h1>

      <div style={{ marginBottom: 12 }}>
        {ALL_ROOMS.map(id => (
          <button key={id} onClick={() => joinRoom(id)} disabled={joinedRooms.includes(id)}>
            {id}번 방 입장
          </button>
        ))}
      </div>

      {joinedRooms.length === 0 && <p>참여 중인 방이 없습니다.</p>}

      {joinedRooms.map(id => (
        <ChatRoom key={id} roomId={id} onLeave={leaveRoom} />   
      ))}
    </div>
  );
}

export default App;