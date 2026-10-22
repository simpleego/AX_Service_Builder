// ============================================================
// 11. 종합: 할 일 앱의 "두뇌"를 순수 자바스크립트로 만들기
// 실행: node lessons/11-todo-logic.js
// ============================================================
// 지금까지 배운 것(함수, 객체, 배열, 불변성, 비동기)을 모아
// React 할 일 앱이 하는 일을 화면 없이 그대로 해 봅니다.
// 이 함수들은 React로 옮겨도 거의 그대로 쓸 수 있습니다.

// ── 1. 상태를 바꾸는 순수 함수들 ────────────────────────────
// 규칙: 받은 배열을 고치지 않고, 항상 새 배열을 돌려준다.

function addTodo(todos, title, priority = 'medium') {
  const trimmed = title.trim();
  if (!trimmed) return todos; // 빈 제목이면 그대로 (변화 없음)
  const nextId = todos.length === 0 ? 1 : Math.max(...todos.map(t => t.id)) + 1;
  return [...todos, { id: nextId, title: trimmed, done: false, priority }];
}

function toggleTodo(todos, id) {
  return todos.map(t => (t.id === id ? { ...t, done: !t.done } : t));
}

function renameTodo(todos, id, title) {
  return todos.map(t => (t.id === id ? { ...t, title: title.trim() } : t));
}

function removeTodo(todos, id) {
  return todos.filter(t => t.id !== id);
}

function clearCompleted(todos) {
  return todos.filter(t => !t.done);
}

function toggleAll(todos) {
  const allDone = todos.every(t => t.done);
  return todos.map(t => ({ ...t, done: !allDone }));
}

// ── 2. 상태로부터 "계산"하는 함수들 (파생 값) ───────────────
function filterTodos(todos, filter) {
  if (filter === 'active') return todos.filter(t => !t.done);
  if (filter === 'done') return todos.filter(t => t.done);
  return todos;
}

function searchTodos(todos, keyword) {
  const q = keyword.trim().toLowerCase();
  if (!q) return todos;
  return todos.filter(t => t.title.toLowerCase().includes(q));
}

function countByFilter(todos) {
  const active = todos.filter(t => !t.done).length;
  return { all: todos.length, active, done: todos.length - active };
}

// ── 3. 화면 대신 콘솔에 그리기 ──────────────────────────────
// React에서는 이 함수가 JSX를 돌려주는 컴포넌트가 된다.
function render(todos, filter = 'all', keyword = '') {
  const counts = countByFilter(todos);
  const visible = searchTodos(filterTodos(todos, filter), keyword);
  const lines = [`  할 일 (${counts.active}개 남음) | 필터: ${filter}${keyword ? ` | 검색: ${keyword}` : ''}`];
  if (visible.length === 0) lines.push('  (표시할 항목이 없습니다)');
  for (const t of visible) lines.push(`  ${t.done ? '[x]' : '[ ]'} #${t.id} ${t.title} (${t.priority})`);
  console.log(lines.join('\n'));
}

// ── 4. 사용자 행동 흉내 내기 ────────────────────────────────
let state = []; // React에서는 const [state, setState] = useState([])

console.log('① 할 일 세 개 추가');
state = addTodo(state, '장보기', 'low');
state = addTodo(state, '  React 공부  ', 'high');
state = addTodo(state, '운동하기');
state = addTodo(state, '   '); // 빈 제목은 무시된다
render(state);

console.log('\n② 2번 완료 체크');
state = toggleTodo(state, 2);
render(state);

console.log('\n③ "진행 중" 필터');
render(state, 'active');

console.log('\n④ "공부" 검색');
render(state, 'all', '공부');

console.log('\n⑤ 3번 제목 수정, 1번 삭제');
state = renameTodo(state, 3, '저녁 운동하기');
state = removeTodo(state, 1);
render(state);

console.log('\n⑥ 전체 완료 → 완료 항목 지우기');
state = toggleAll(state);
render(state);
state = clearCompleted(state);
render(state);

// ── 5. 불변성 확인 ─────────────────────────────────────────
const before = [{ id: 1, title: 'A', done: false, priority: 'low' }];
const after = toggleTodo(before, 1);
console.log('\n⑦ 원본은 그대로인가?', before[0].done === false, '/ 새 배열인가?', before !== after); // true / true

// ============================================================
// React로 옮기면
// ------------------------------------------------------------
// const [todos, setTodos] = useState([]);
// const handleAdd    = title => setTodos(prev => addTodo(prev, title));
// const handleToggle = id    => setTodos(prev => toggleTodo(prev, id));
// const visible = searchTodos(filterTodos(todos, filter), keyword);  ← 렌더링 중 계산
// return <ul>{visible.map(t => <TodoItem key={t.id} todo={t} onToggle={handleToggle} />)}</ul>;
// ============================================================
