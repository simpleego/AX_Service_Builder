// ============================================================
// 06. 참조와 불변성 (React에서 가장 많이 틀리는 부분)
// 실행: node lessons/06-immutability.js
// ============================================================
// React는 state가 "바뀌었는지"를 === 로 확인합니다.
// 객체·배열은 내용을 고쳐도 === 결과가 같아서, React는 "안 바뀌었다"고 판단하고
// 화면을 다시 그리지 않습니다. 그래서 항상 "새로 만들어서" 바꿔야 합니다.

// ── 1. 기본 자료형은 값이 복사된다 ──────────────────────────
let a = 10;
let b = a; // 값 10이 복사됨
b = 20;
console.log('[1] 숫자 복사:', a, b); // 10 20 ← a는 그대로

// ── 2. 객체·배열은 "주소(참조)"가 복사된다 ─────────────────
const original = { title: '공부', done: false };
const same = original; // 같은 상자를 가리키는 이름표가 하나 더 생김
same.done = true;
console.log('\n[2] 객체 참조');
console.log(original.done);     // true ← 원본도 바뀌었다!
console.log(original === same); // true ← 같은 상자

// ── 3. 내용이 같아도 다른 상자면 다르다 ─────────────────────
console.log('\n[3] === 비교');
console.log({ x: 1 } === { x: 1 }); // false ← 모양은 같지만 다른 상자
console.log([] === []);             // false

// ── 4. React가 화면을 다시 그리는지 흉내 내 보기 ────────────
// React는 대략 이렇게 판단한다: "이전 값 === 새 값 이면 다시 그리지 않는다"
function fakeSetState(prev, next) {
  return prev === next ? '변화 없음 → 다시 그리지 않음' : '바뀜 → 화면 다시 그림';
}

const todos = [{ id: 1, title: '공부', done: false }];

// ❌ 잘못된 방법: 원본을 직접 고치고 같은 배열을 넣는다
todos[0].done = true;
console.log('\n[4] 직접 수정:', fakeSetState(todos, todos)); // 변화 없음 → 다시 그리지 않음

// ✅ 올바른 방법: 새 배열, 새 객체를 만든다
const nextTodos = todos.map(t => (t.id === 1 ? { ...t, done: false } : t));
console.log('    새로 만들기:', fakeSetState(todos, nextTodos)); // 바뀜 → 화면 다시 그림

// ── 5. 자주 쓰는 "새로 만들기" 패턴 정리 ────────────────────
const list = [
  { id: 1, title: 'A', done: false },
  { id: 2, title: 'B', done: true },
];
console.log('\n[5] 패턴');
console.log('추가:', [...list, { id: 3, title: 'C', done: false }].length);   // 3
console.log('삭제:', list.filter(t => t.id !== 1).map(t => t.title));        // [ 'B' ]
console.log('수정:', list.map(t => (t.id === 1 ? { ...t, title: 'A2' } : t))[0].title); // A2
console.log('맨 앞 추가:', [{ id: 0, title: 'Z', done: false }, ...list][0].title); // Z
console.log('원본:', list.map(t => t.title)); // [ 'A', 'B' ] ← 위 작업 후에도 원본 그대로

// ── 6. 얕은 복사의 함정 ─────────────────────────────────────
// ... 는 "한 층"만 복사한다. 안쪽 객체는 여전히 같은 상자다.
const user = { name: '민수', settings: { theme: 'light' } };
const copy = { ...user };
copy.settings.theme = 'dark';
console.log('\n[6] 얕은 복사');
console.log(user.settings.theme); // dark ← 원본의 안쪽까지 바뀌었다!

// ✅ 안쪽까지 바꿀 때는 바꾸는 층마다 펼친다
const user2 = { name: '민수', settings: { theme: 'light' } };
const updated = { ...user2, settings: { ...user2.settings, theme: 'dark' } };
console.log(user2.settings.theme, updated.settings.theme); // light dark

// ── 7. const는 "다시 넣기"만 막는다 ─────────────────────────
const arr = [1, 2];
arr.push(3); // 에러가 나지 않는다! const는 내용 변경까지 막지는 않는다
console.log('\n[7] const 배열:', arr); // [ 1, 2, 3 ]
// arr = [];  // ← 이것만 에러

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// ❌ todos.push(newTodo); setTodos(todos);          → 화면이 안 바뀜
// ✅ setTodos([...todos, newTodo]);
// ❌ todo.done = true; setTodos(todos);
// ✅ setTodos(todos.map(t => t.id === id ? { ...t, done: true } : t));
// v2 낙관적 업데이트: old?.map(t => (t.id === id ? { ...t, ...patch } : t))
// ============================================================
