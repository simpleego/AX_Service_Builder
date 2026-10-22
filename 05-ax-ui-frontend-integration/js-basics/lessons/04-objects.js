// ============================================================
// 04. 객체
// 실행: node lessons/04-objects.js
// ============================================================
// 객체 = 이름(키)과 값을 묶은 꾸러미. 할 일 하나, 사용자 한 명이 객체입니다.
// React의 props도 객체입니다.

// ── 1. 만들기와 읽기 ────────────────────────────────────────
const todo = {
  id: 1,
  title: 'React 공부',
  done: false,
  priority: 'high',
};
console.log('[1] 읽기');
console.log(todo.title);      // React 공부  ← 점 표기법
console.log(todo['priority']); // high       ← 대괄호 표기법 (키를 변수로 쓸 때)
const key = 'done';
console.log(todo[key]);        // false
console.log(todo.memo);        // undefined ← 없는 키를 읽으면 undefined

// ── 2. 단축 속성 ────────────────────────────────────────────
// 변수 이름과 키 이름이 같으면 한 번만 쓴다
const title = '운동하기';
const done = true;
const short = { title, done };          // { title: title, done: done } 와 같다
console.log('\n[2] 단축 속성:', short); // { title: '운동하기', done: true }

// ── 3. 구조 분해 할당 (React에서 매일 씀!) ──────────────────
// 객체에서 필요한 값만 꺼내 같은 이름의 변수로 만든다
const { id, priority } = todo;
console.log('\n[3] 구조 분해:', id, priority); // 1 high

// 이름 바꾸기와 기본값
const { title: todoTitle, memo = '(메모 없음)' } = todo;
console.log(todoTitle, memo); // React 공부 (메모 없음)

// 함수 매개변수에서 바로 구조 분해 ← React 컴포넌트가 props를 받는 방식
function TodoItem({ title, done }) {
  return `${done ? '[x]' : '[ ]'} ${title}`;
}
console.log(TodoItem(todo)); // [ ] React 공부

// ── 4. 전개 연산자 ... (복사하면서 일부만 바꾸기) ───────────
const updated = { ...todo, done: true }; // todo를 펼쳐 복사한 뒤 done만 덮어쓴다
console.log('\n[4] 전개 연산자');
console.log(updated);     // { id: 1, title: 'React 공부', done: true, priority: 'high' }
console.log(todo.done);   // false ← 원본은 그대로!

// 순서가 중요하다: 뒤에 오는 것이 이긴다
console.log({ done: true, ...todo }.done); // false ← todo의 done이 뒤에서 덮어씀

// 두 객체 합치기
const defaults = { priority: 'medium', memo: '' };
const input = { title: '새 할 일', priority: 'low' };
console.log({ ...defaults, ...input }); // { priority: 'low', memo: '', title: '새 할 일' }

// ── 5. 계산된 속성 이름 [ ] ─────────────────────────────────
// 키 이름을 변수로 정한다. 입력칸 여러 개를 함수 하나로 처리할 때 쓴다.
function updateField(form, name, value) {
  return { ...form, [name]: value };
}
const form = { title: '', priority: 'medium' };
console.log('\n[5] 계산된 속성');
console.log(updateField(form, 'title', '공부'));    // { title: '공부', priority: 'medium' }
console.log(updateField(form, 'priority', 'high')); // { title: '', priority: 'high' }

// ── 6. 객체 순회 ────────────────────────────────────────────
const labels = { high: '높음', medium: '보통', low: '낮음' };
console.log('\n[6] 순회');
console.log(Object.keys(labels));    // [ 'high', 'medium', 'low' ]
console.log(Object.values(labels));  // [ '높음', '보통', '낮음' ]
console.log(Object.entries(labels)); // [ [ 'high', '높음' ], [ 'medium', '보통' ], [ 'low', '낮음' ] ]
// 에러가 몇 개인지 세기
const errors = { title: '제목을 입력하세요.' };
console.log(Object.keys(errors).length > 0 ? '에러 있음' : '통과'); // 에러 있음

// ── 7. 객체 안의 객체, 옵셔널 체이닝 ────────────────────────
const user = { name: '민수', address: { city: '서울' } };
console.log('\n[7] 중첩');
console.log(user.address.city);   // 서울
console.log(user.company?.name);  // undefined ← company가 없어도 에러가 나지 않는다

// ── 8. JSON: 객체 ↔ 문자열 ──────────────────────────────────
// 서버와 주고받거나 localStorage에 저장할 때는 문자열로 바꿔야 한다
const json = JSON.stringify(todo);
console.log('\n[8] JSON');
console.log(json);              // {"id":1,"title":"React 공부","done":false,"priority":"high"}
console.log(typeof json);       // string
const back = JSON.parse(json);
console.log(back.title);        // React 공부

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// props 받기:      function TodoItem({ todo, onToggle, onDelete }) { … }
// 하나만 바꾸기:   todos.map(t => t.id === id ? { ...t, done: !t.done } : t)
// 입력칸 처리:     setValues(prev => ({ ...prev, [name]: value }))       (v2 TodoForm)
// 옵션 목록 만들기: Object.entries(PRIORITY_LABEL).map(([value, label]) => <option …>)
// 서버 전송:       body: JSON.stringify(input)
// ============================================================
