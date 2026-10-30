import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import ConfirmPractice from './chapter_08.jsx';
import LoginPractice from './chapter_09.jsx';
import AttendancePractice from './chapter_10.jsx';
import SignUpPractice from './chapter_11.jsx';
import TemperaturePractice from './chapter_12.jsx';
import CompositionPractice from './chapter_13.jsx';
import ContextPractice from './chapter_14.jsx';
import StylePractice from './chapter_15.jsx';
import './style.css';

const lessons = [
  ['08 이벤트', ConfirmPractice], ['09 조건부 렌더링', LoginPractice],
  ['10 리스트와 key', AttendancePractice], ['11 폼', SignUpPractice],
  ['12 상태 끌어올리기', TemperaturePractice], ['13 합성', CompositionPractice],
  ['14 Context', ContextPractice], ['15 스타일링', StylePractice],
];
function App() {
  const [selected, setSelected] = useState(0);
  const Lesson = lessons[selected][1];
  return <><header><h1>React 08–15 실습실</h1>
    <p>챕터를 바꾸면 해당 실습 상태가 초기화됩니다.</p>
    <nav aria-label="챕터 선택">{lessons.map(([title], index) =>
      <button key={title} aria-pressed={selected === index} onClick={() => setSelected(index)}>{title}</button>
    )}</nav></header><main><h2>{lessons[selected][0]}</h2><Lesson key={selected} /></main></>;
}
createRoot(document.getElementById('root')).render(<React.StrictMode><App /></React.StrictMode>);
