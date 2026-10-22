// ============================================================
// 연습 11. 종합: 할 일 앱의 두뇌 만들기
// 실행: node exercises/11-todo-logic.js   (정답: solutions/11-todo-logic.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// 이 함수들이 모두 통과하면, React 할 일 앱에 필요한 자바스크립트는 준비된 것입니다.
// 공통 규칙: 받은 배열을 고치지 말고 새 배열을 돌려주세요.
// 할 일 모양: { id: 숫자, title: 문자열, done: 불리언 }
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 제목의 앞뒤 공백을 지우고 할 일을 끝에 추가하세요.
//         - 제목이 공백뿐이면 받은 배열을 그대로 돌려주세요.
//         - 새 id는 "현재 가장 큰 id + 1", 목록이 비었으면 1
export function addTodo(todos, title) {
  // ▼
  const trimmed = title.trim();
  if (!trimmed) return todos;
  const nextId = todos.length === 0 ? 1 : Math.max(...todos.map(t => t.id)) + 1;
  return [...todos, { id: nextId, title: trimmed, done: false }];
  // ▲
}

// 문제 2. id가 같은 할 일의 done을 반대로
export function toggleTodo(todos, id) {
  // ▼
  return todos.map(t => (t.id === id ? { ...t, done: !t.done } : t));
  // ▲
}

// 문제 3. id가 같은 할 일의 제목을 바꾸기 (앞뒤 공백 제거, 빈 제목이면 바꾸지 않음)
export function renameTodo(todos, id, title) {
  // ▼
  const trimmed = title.trim();
  if (!trimmed) return todos;
  return todos.map(t => (t.id === id ? { ...t, title: trimmed } : t));
  // ▲
}

// 문제 4. id가 같은 할 일 삭제
export function removeTodo(todos, id) {
  // ▼
  return todos.filter(t => t.id !== id);
  // ▲
}

// 문제 5. 필터: 'all' 전체, 'active' 진행 중, 'done' 완료
export function filterTodos(todos, filter) {
  // ▼
  if (filter === 'active') return todos.filter(t => !t.done);
  if (filter === 'done') return todos.filter(t => t.done);
  return todos;
  // ▲
}

// 문제 6. 개수 세기: { all: 전체, active: 진행 중, done: 완료 }
export function countByFilter(todos) {
  // ▼
  const active = todos.filter(t => !t.done).length;
  return { all: todos.length, active, done: todos.length - active };
  // ▲
}

// 문제 7. 완료된 할 일을 모두 지우기
export function clearCompleted(todos) {
  // ▼
  return todos.filter(t => !t.done);
  // ▲
}

// 문제 8. 전체 완료 토글: 모두 완료 상태면 모두 해제, 하나라도 미완료면 모두 완료
export function toggleAll(todos) {
  // ▼
  const allDone = todos.every(t => t.done);
  return todos.map(t => ({ ...t, done: !allDone }));
  // ▲
}

// ── 채점 ─────────────────────────────────────────────────────
const titles = list => list.map(t => t.title);
const start = () => [
  { id: 1, title: '장보기', done: false },
  { id: 5, title: 'React 공부', done: true },
];

check('1-1. 추가 (공백 제거, id = 최대값 + 1)', () => addTodo(start(), '  운동  ').at(-1), { id: 6, title: '운동', done: false });
check('1-2. 빈 목록에 추가', () => addTodo([], '첫 할 일'), [{ id: 1, title: '첫 할 일', done: false }]);
check('1-3. 빈 제목은 무시 (같은 배열 그대로)', () => {
  const list = start();
  return addTodo(list, '   ') === list;
}, true);
check('2. 토글', () => toggleTodo(start(), 1).map(t => t.done), [true, true]);
check('3-1. 제목 수정', () => titles(renameTodo(start(), 5, ' Vue 공부 ')), ['장보기', 'Vue 공부']);
check('3-2. 빈 제목으로는 수정 안 됨', () => titles(renameTodo(start(), 5, '  ')), ['장보기', 'React 공부']);
check('4. 삭제', () => removeTodo(start(), 1).map(t => t.id), [5]);
check('5. 필터', () => [filterTodos(start(), 'all').length, titles(filterTodos(start(), 'active')), titles(filterTodos(start(), 'done'))], [2, ['장보기'], ['React 공부']]);
check('6. 개수', () => countByFilter(start()), { all: 2, active: 1, done: 1 });
check('7. 완료 지우기', () => titles(clearCompleted(start())), ['장보기']);
check('8-1. 하나라도 미완료 → 모두 완료', () => toggleAll(start()).map(t => t.done), [true, true]);
check('8-2. 모두 완료 → 모두 해제', () => toggleAll(toggleAll(start())).map(t => t.done), [false, false]);
check('9. 원본을 고치지 않았나? (모든 함수)', () => {
  const list = start();
  const snapshot = JSON.stringify(list);
  const outputs = [
    addTodo(list, 'x'),
    toggleTodo(list, 1),
    renameTodo(list, 1, 'y'),
    removeTodo(list, 1),
    clearCompleted(list),
    toggleAll(list),
  ];
  const allArrays = outputs.every(Array.isArray); // 모두 배열을 돌려줬는지
  return allArrays && JSON.stringify(list) === snapshot;
}, true);
summary();
