# useRef 사용 예시

`useRef`는 **렌더링과 상관없이 값을 계속 기억해 두는 상자**입니다. `.current` 속성에 값을 넣고 꺼내 쓰며, 값이 바뀌어도 **화면을 다시 그리지 않습니다**. 크게 두 가지로 씁니다.

- **DOM 요소에 직접 접근할 때** (포커스, 스크롤, 크기 측정, 미디어 재생)
- **리렌더링 없이 값을 보관할 때** (타이머 ID, 이전 값, 외부 라이브러리 객체)

대표적인 경우 6가지를 예시와 함께 정리했습니다.

---

## 1. 입력창에 자동 포커스 주기

화면이 뜨자마자, 또는 버튼을 누르면 입력창에 커서를 둡니다.

```jsx
import { useRef, useEffect } from 'react';

function LoginForm() {
  const idRef = useRef(null);

  useEffect(() => {
    idRef.current.focus(); // 처음 렌더링되면 아이디 입력창에 포커스
  }, []);

  return (
    <form>
      <input ref={idRef} placeholder="아이디" />
      <input type="password" placeholder="비밀번호" />
      <button type="button" onClick={() => idRef.current.focus()}>
        아이디 다시 입력
      </button>
    </form>
  );
}
```

## 2. 특정 위치로 스크롤하기

버튼을 누르면 원하는 요소가 보이도록 스크롤합니다. 새 메시지가 오면 맨 아래로 내리는 채팅창에도 씁니다.

```jsx
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
```

## 3. 타이머 ID 보관하기 (스톱워치)

시작할 때 받은 타이머 ID를 기억해 두었다가, 정지할 때 꺼내 씁니다. ID는 화면에 보여 줄 값이 아니므로 state 대신 ref에 둡니다.

```jsx
import { useState, useRef } from 'react';

function Stopwatch() {
  const [time, setTime] = useState(0);
  const timerRef = useRef(null);

  const start = () => {
    if (timerRef.current) return; // 이미 실행 중이면 무시
    timerRef.current = setInterval(() => setTime(t => t + 1), 1000);
  };

  const stop = () => {
    clearInterval(timerRef.current);
    timerRef.current = null;
  };

  const reset = () => {
    stop();
    setTime(0);
  };

  return (
    <div>
      <p>{time}초</p>
      <button onClick={start}>시작</button>
      <button onClick={stop}>정지</button>
      <button onClick={reset}>초기화</button>
    </div>
  );
}
```

## 4. 이전 값 기억하기

값이 바뀌기 전의 값을 기억해 두고 현재 값과 비교합니다.

```jsx
import { useState, useRef, useEffect } from 'react';

function PriceTracker() {
  const [price, setPrice] = useState(1000);
  const prevPriceRef = useRef(price);

  useEffect(() => {
    prevPriceRef.current = price; // 렌더링이 끝난 뒤 현재 값을 저장합니다
  }, [price]);

  const prev = prevPriceRef.current; // 렌더링 중에는 아직 이전 값입니다
  const diff = price - prev;

  return (
    <div>
      <p>현재 가격: {price}원 (이전: {prev}원)</p>
      <p>{diff > 0 ? `▲ ${diff}` : diff < 0 ? `▼ ${-diff}` : '변동 없음'}</p>
      <button onClick={() => setPrice(p => p + 100)}>+100</button>
      <button onClick={() => setPrice(p => p - 100)}>-100</button>
    </div>
  );
}
```

## 5. 리렌더링 없이 횟수 세기

클릭 횟수처럼 기록만 하고 화면에는 보여 줄 필요가 없는 값을 셉니다.

```jsx
import { useState, useRef } from 'react';

function ClickLogger() {
  const [text, setText] = useState('');
  const clickCount = useRef(0); // 바뀌어도 화면이 다시 그려지지 않습니다

  const handleClick = () => {
    clickCount.current += 1;
    console.log(`버튼 클릭 ${clickCount.current}번`);
  };

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={handleClick}>클릭 (콘솔 확인)</button>
    </div>
  );
}
```

## 6. 비디오 재생 제어하기

`<video>` 요소의 `play()`, `pause()` 같은 브라우저 기능을 직접 호출합니다.

```jsx
import { useState, useRef } from 'react';

function VideoPlayer({ src }) {
  const videoRef = useRef(null);
  const [playing, setPlaying] = useState(false);

  const toggle = () => {
    if (playing) {
      videoRef.current.pause();
    } else {
      videoRef.current.play();
    }
    setPlaying(!playing);
  };

  return (
    <div>
      <video ref={videoRef} src={src} width={400} />
      <button onClick={toggle}>{playing ? '일시정지' : '재생'}</button>
    </div>
  );
}
```

---

## 정리: useRef와 useState 비교

| 구분 | useState | useRef |
|---|---|---|
| 값이 바뀌면 | 화면을 다시 그림 | 화면을 다시 그리지 않음 |
| 값 읽기·쓰기 | `value`, `setValue(새값)` | `ref.current` |
| 바꾼 값이 반영되는 시점 | 다음 렌더링 | 즉시 |
| 주 용도 | 화면에 보여 줄 값 | DOM 접근, 화면에 안 보이는 값 |

| 경우 | ref에 담는 것 |
|---|---|
| 자동 포커스 | `<input>` 요소 |
| 스크롤 이동 | 목표 위치의 요소 |
| 스톱워치 | 타이머 ID |
| 이전 값 기억 | 직전 렌더링의 값 |
| 횟수 세기 | 숫자 |
| 비디오 제어 | `<video>` 요소 |

## 주의할 점

- **렌더링 중에는 `ref.current`를 읽거나 쓰지 않는 것이 원칙입니다.** 이벤트 핸들러나 `useEffect` 안에서 다룹니다. (예시 4처럼 이전 값을 보여 주는 용도는 예외적으로 쓰입니다.)
- **화면에 보여야 하는 값은 useState를 씁니다.** ref 값을 바꿔도 화면은 그대로입니다.
- DOM ref는 첫 렌더링 중에는 `null`입니다. 화면에 그려진 뒤(`useEffect`, 이벤트 핸들러)에 사용합니다.
