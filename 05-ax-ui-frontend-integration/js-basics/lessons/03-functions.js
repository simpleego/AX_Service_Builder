// ============================================================
// 03. 함수
// 실행: node lessons/03-functions.js
// ============================================================
// React 컴포넌트는 "함수"입니다. 버튼을 눌렀을 때 할 일도 "함수"입니다.
// 함수를 이해하면 React의 절반을 이해한 것입니다.

// ── 1. 함수 선언과 호출 ─────────────────────────────────────
// 입력(매개변수)을 받아 결과(return)를 돌려주는 기계
function add(a, b) {
  return a + b;
}
console.log('[1] 함수 호출:', add(2, 3)); // 5

// return이 없으면 undefined를 돌려준다
function sayHi(name) {
  console.log(`안녕하세요, ${name}님`);
}
const result = sayHi('학생'); // 안녕하세요, 학생님
console.log('return 없는 함수의 결과:', result); // undefined

// ── 2. 화살표 함수 ──────────────────────────────────────────
// React 코드에서 가장 많이 보는 모양. function 대신 => 를 쓴다.
const multiply = (a, b) => {
  return a * b;
};
// 본문이 한 줄(값 하나)이면 { } 와 return 을 생략할 수 있다
const double = n => n * 2;          // 매개변수가 하나면 괄호도 생략 가능
const getZero = () => 0;            // 매개변수가 없으면 () 를 쓴다
// 객체를 바로 돌려줄 때는 ( ) 로 감싼다. 안 감싸면 { }를 함수 본문으로 착각한다
const makeTodo = title => ({ title, done: false });

console.log('\n[2] 화살표 함수');
console.log(multiply(3, 4)); // 12
console.log(double(5));      // 10
console.log(getZero());      // 0
console.log(makeTodo('공부')); // { title: '공부', done: false }

// ── 3. 매개변수 기본값 ──────────────────────────────────────
const greet = (name = '손님') => `${name}님 환영합니다`;
console.log('\n[3] 기본값');
console.log(greet());       // 손님님 환영합니다
console.log(greet('민수')); // 민수님 환영합니다

// ── 4. 함수도 "값"이다 ──────────────────────────────────────
// 함수를 변수에 담고, 다른 함수에 넘기고, 함수에서 돌려줄 수 있다.
// 이것이 React의 이벤트 처리와 props 전달의 기초다.
const sayBye = () => '안녕히 가세요';
const fn = sayBye;   // 함수 자체를 담는다 (괄호 없음!)
const text = sayBye(); // 함수를 "실행한 결과"를 담는다 (괄호 있음)
console.log('\n[4] 함수 vs 함수 실행 결과');
console.log(typeof fn);   // function
console.log(typeof text); // string

// [중요] React에서 자주 하는 실수
//   <button onClick={handleClick}>     ← 함수를 넘긴다 (클릭할 때 실행됨) ✅
//   <button onClick={handleClick()}>   ← 화면을 그릴 때 바로 실행해 버린다 ❌
//   <button onClick={() => remove(id)}> ← 값을 넣어 실행하고 싶으면 화살표 함수로 감싼다 ✅

// ── 5. 콜백 함수 ────────────────────────────────────────────
// "나중에 불러 달라"고 다른 함수에 넘기는 함수
function runTwice(callback) {
  callback(1);
  callback(2);
}
console.log('\n[5] 콜백');
runTwice(n => console.log(`${n}번째 실행`)); // 1번째 실행 / 2번째 실행

// 버튼 흉내 내기: 클릭 시 실행할 함수를 미리 등록해 둔다
function createButton(label, onClick) {
  return {
    label,
    click: () => onClick(label), // 클릭되면 등록된 함수를 부른다
  };
}
const button = createButton('저장', name => console.log(`"${name}" 버튼 클릭됨`));
button.click(); // "저장" 버튼 클릭됨

// ── 6. 일찍 돌아가기 (early return) ─────────────────────────
// 조건이 안 맞으면 함수 앞부분에서 바로 끝낸다. 중첩 if를 줄여 읽기 쉽다.
function addTodoTitle(title) {
  if (!title.trim()) return '제목을 입력하세요.';
  if (title.length > 50) return '50자 이하로 입력하세요.';
  return `추가됨: ${title.trim()}`;
}
console.log('\n[6] early return');
console.log(addTodoTitle('   '));     // 제목을 입력하세요.
console.log(addTodoTitle('공부하기')); // 추가됨: 공부하기

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// 컴포넌트 자체가 함수: export default function App() { return <main>…</main>; }
// 이벤트 핸들러:        <button onClick={() => onDelete(todo.id)}>삭제</button>
// props로 함수 전달:     <TodoForm onAdd={addTodo} />   → 자식이 onAdd(text) 를 부른다
// early return:         if (isPending) return <Loading />;
// ============================================================
