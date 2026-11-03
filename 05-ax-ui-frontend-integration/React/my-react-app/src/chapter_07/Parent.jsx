import { useState, useCallback, memo } from 'react';

function Parent() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState('');
  console.log('Component called...')

  function test(){
    console.log('function called')
  }

  test();

  // text를 입력해도 handleClick은 같은 함수로 유지됩니다
  const handleClick = useCallback(() => {
    setCount(c => c + 1);
    console.log('called...')  
  }, []);

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <p>count: {count}</p>
      <CountButton onClick={handleClick} />
    </div>
  );
}

const CountButton = memo(({ onClick }) => {
  console.log('CountButton 렌더링'); // 입력할 때는 찍히지 않습니다
  return <button onClick={onClick}>+1</button>;
});

export default Parent;