import { useState, useEffect } from 'react';

function TodoInput() {
  // 초기값은 localStorage에서 읽어옵니다
  const [text, setText] = useState(() => localStorage.getItem('draft') ?? '');

  useEffect(() => {
    console.log('저장전 호출됨')
    localStorage.setItem('draft', text);
    console.log('저장후 호출됨')
  }, [text]);

  return <input value={text} onChange={e => setText(e.target.value)} placeholder="임시 저장됩니다" />;
}

export default TodoInput;