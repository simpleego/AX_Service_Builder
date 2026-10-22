// ============================================================
// 05. 배열과 배열 메서드
// 실행: node lessons/05-arrays.js
// ============================================================
// 목록 화면 = 배열을 화면 요소로 바꾸는 일입니다.
// map, filter, find 세 가지만 확실히 알아도 React 목록은 다 만들 수 있습니다.

const todos = [
  { id: 1, title: '장보기', done: false, priority: 'low' },
  { id: 2, title: 'React 공부', done: true, priority: 'high' },
  { id: 3, title: '운동하기', done: false, priority: 'medium' },
];

// ── 1. 기본 ────────────────────────────────────────────────
console.log('[1] 기본');
console.log(todos.length);      // 3
console.log(todos[0].title);    // 장보기  ← 번호(index)는 0부터
console.log(todos.at(-1).title); // 운동하기 ← 마지막 항목

// ── 2. map: 각 항목을 "바꿔서" 새 배열 만들기 ───────────────
// 결과 배열의 길이는 원래와 같다
const titles = todos.map(todo => todo.title);
console.log('\n[2] map');
console.log(titles); // [ '장보기', 'React 공부', '운동하기' ]

// 화면 요소처럼 문자열로 바꾸기 (React에서는 문자열 대신 <li>를 만든다)
const lines = todos.map(todo => `<li>${todo.title}</li>`);
console.log(lines.join('\n'));

// 하나만 바꾸고 나머지는 그대로 ← 완료 체크할 때 쓰는 패턴
const toggled = todos.map(t => (t.id === 1 ? { ...t, done: !t.done } : t));
console.log(toggled[0].done, todos[0].done); // true false ← 원본은 그대로

// ── 3. filter: 조건에 맞는 것만 "골라서" 새 배열 만들기 ──────
const active = todos.filter(todo => !todo.done);
console.log('\n[3] filter');
console.log(active.map(t => t.title)); // [ '장보기', '운동하기' ]

// 하나 빼기 ← 삭제할 때 쓰는 패턴
const removed = todos.filter(t => t.id !== 2);
console.log(removed.length); // 2

// 검색
const keyword = '공부';
console.log(todos.filter(t => t.title.includes(keyword)).length); // 1

// ── 4. find / findIndex / some / every / includes ───────────
console.log('\n[4] 찾기와 검사');
console.log(todos.find(t => t.id === 3));        // { id: 3, title: '운동하기', … } ← 첫 번째 하나
console.log(todos.find(t => t.id === 99));       // undefined ← 없으면 undefined
console.log(todos.findIndex(t => t.id === 3));   // 2
console.log(todos.some(t => t.done));            // true  ← 하나라도 맞으면
console.log(todos.every(t => t.done));           // false ← 모두 맞아야
console.log(['all', 'active', 'done'].includes('done')); // true

// ── 5. reduce: 배열을 값 하나로 "모으기" ────────────────────
// (누적값, 현재항목) => 새 누적값, 처음 누적값
const doneCount = todos.reduce((sum, t) => (t.done ? sum + 1 : sum), 0);
console.log('\n[5] reduce:', doneCount); // 1
// 사실 이 경우는 filter(...).length 가 더 읽기 쉽다. reduce는 꼭 필요할 때만.
console.log(todos.filter(t => t.done).length); // 1

// ── 6. 메서드 이어 쓰기 (체이닝) ────────────────────────────
const result = todos
  .filter(t => !t.done)
  .map(t => t.title.toUpperCase());
console.log('\n[6] 체이닝:', result); // [ '장보기', '운동하기' ]

// ── 7. 원본을 바꾸는 메서드 주의! ───────────────────────────
// push, pop, splice, sort, reverse 는 "원본"을 바꾼다.
// React의 state 배열에는 쓰지 말고, 새 배열을 만드는 방법을 쓴다.
const numbers = [3, 1, 2];
const sortedCopy = [...numbers].sort((a, b) => a - b); // 복사한 뒤 정렬
console.log('\n[7] 정렬');
console.log(sortedCopy, numbers); // [ 1, 2, 3 ] [ 3, 1, 2 ]

// 추가하기: push 대신 전개 연산자
const added = [...todos, { id: 4, title: '독서', done: false, priority: 'low' }];
console.log(added.length, todos.length); // 4 3

// ── 8. 배열 구조 분해 ───────────────────────────────────────
// 순서대로 꺼낸다. React의 useState가 바로 이 모양이다.
const [first, second] = ['사과', '바나나', '포도'];
console.log('\n[8] 배열 구조 분해:', first, second); // 사과 바나나

function useCounter() {
  let value = 0;
  const setValue = next => (value = next);
  return [value, setValue]; // [값, 바꾸는함수]
}
const [count, setCount] = useCounter();
console.log(count, typeof setCount); // 0 function

// Object.entries 와 함께
for (const [key, label] of Object.entries({ high: '높음', low: '낮음' })) {
  console.log(`${key} → ${label}`);
}

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// 목록 그리기:   {visible.map(todo => <TodoItem key={todo.id} todo={todo} />)}
// 추가:          setTodos([...todos, newTodo])
// 완료 체크:     setTodos(todos.map(t => t.id === id ? { ...t, done: !t.done } : t))
// 삭제:          setTodos(todos.filter(t => t.id !== id))
// 남은 개수:     todos.filter(t => !t.done).length
// state 꺼내기:  const [todos, setTodos] = useState([]);
// ============================================================
