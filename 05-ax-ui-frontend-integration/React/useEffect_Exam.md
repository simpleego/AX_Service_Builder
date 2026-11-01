# useEffect 사용 예시

`useEffect`는 **렌더링 결과를 React 바깥 세계(서버, 브라우저 API, 타이머, 외부 라이브러리 등)와 맞출 때** 씁니다. 대표적인 경우 6가지를 예시와 함께 정리했습니다.

---

## 1. 서버에서 데이터 가져오기 (API 호출)

화면이 처음 뜰 때나 특정 값(예: `userId`)이 바뀔 때 데이터를 불러옵니다.

```jsx
import { useState, useEffect } from 'react';

function UserProfile({ userId }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    let ignore = false; // 이전 요청 응답이 늦게 도착해 덮어쓰는 것을 막습니다

    fetch(`https://jsonplaceholder.typicode.com/users/${userId}`)
      .then(res => res.json())
      .then(data => { if (!ignore) setUser(data); });

    return () => { ignore = true; };
  }, [userId]); // userId가 바뀔 때마다 다시 요청합니다

  if (!user) return <p>로딩 중...</p>;
  return <h2>{user.name}</h2>;
}
```

## 2. 타이머 설정과 정리 (setInterval / setTimeout)

타이머를 시작하고, 컴포넌트가 사라질 때 반드시 정리(cleanup)합니다.

```jsx
import { useState, useEffect } from 'react';

function Clock() {
  const [now, setNow] = useState(new Date());

  useEffect(() => {
    const id = setInterval(() => setNow(new Date()), 1000);
    return () => clearInterval(id); // 정리하지 않으면 타이머가 계속 쌓입니다
  }, []);

  return <p>현재 시각: {now.toLocaleTimeString()}</p>;
}
```

## 3. 브라우저 이벤트 등록 (resize, scroll, keydown)

`window`나 `document`에 이벤트를 붙이고, 사라질 때 떼어냅니다.

```jsx
import { useState, useEffect } from 'react';

function WindowSize() {
  const [width, setWidth] = useState(window.innerWidth);

  useEffect(() => {
    const handleResize = () => setWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);

    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return <p>창 너비: {width}px</p>;
}
```

## 4. 문서 제목 바꾸기 (document.title)

상태 값에 맞춰 브라우저 탭 제목을 바꿉니다.

```jsx
import { useState, useEffect } from 'react';

function NotificationTitle() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    document.title = count > 0 ? `(${count}) 새 알림` : '알림 없음';
  }, [count]); // count가 바뀔 때만 실행합니다

  return <button onClick={() => setCount(c => c + 1)}>알림 추가</button>;
}
```

## 5. localStorage에 저장하기

상태가 바뀔 때마다 브라우저에 저장해서, 새로고침해도 값이 남게 합니다.

```jsx
import { useState, useEffect } from 'react';

function TodoInput() {
  // 초기값은 localStorage에서 읽어옵니다
  const [text, setText] = useState(() => localStorage.getItem('draft') ?? '');

  useEffect(() => {
    localStorage.setItem('draft', text);
  }, [text]);

  return <input value={text} onChange={e => setText(e.target.value)} placeholder="임시 저장됩니다" />;
}
```

## 6. 실시간 연결 구독 (WebSocket, 채팅방)

연결을 열고, 방이 바뀌거나 화면을 떠나면 연결을 닫습니다.

```jsx
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
```

---

## 정리: 실행 흐름

```
렌더링 → 화면 반영 → useEffect 실행
          ↓ (의존성 값이 바뀌면)
     cleanup 실행 → useEffect 다시 실행
          ↓ (컴포넌트가 사라지면)
     cleanup 실행
```

| 경우 | 의존성 배열 | cleanup 필요 |
|---|---|---|
| 데이터 가져오기 | `[userId]` | 권장 (늦게 온 응답 무시) |
| 타이머 | `[]` | **필수** |
| 브라우저 이벤트 | `[]` | **필수** |
| 문서 제목 | `[count]` | 불필요 |
| localStorage 저장 | `[text]` | 불필요 |
| WebSocket 구독 | `[roomId]` | **필수** |

## useEffect가 필요 없는 경우

- **props나 state로 계산할 수 있는 값**은 렌더링 중에 바로 계산합니다.
  `const fullName = first + ' ' + last;` ✅ (useEffect + setState ❌)
- **버튼 클릭 같은 사용자 동작에 대한 처리**는 이벤트 핸들러에 씁니다.
