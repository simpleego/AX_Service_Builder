// ============================================================
// 연습 03. 함수
// 실행: node exercises/03-functions.js   (정답: solutions/03-functions.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 숫자를 제곱해 돌려주는 화살표 함수를 완성하세요.
export const square = n => {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
};

// 문제 2. 이름이 없으면 '손님'을 쓰도록 매개변수 기본값을 활용해 "민수님 환영합니다"를 돌려주세요.
//         (함수 첫 줄의 매개변수 부분은 그대로 두고, 본문만 작성합니다)
export function greet(name = '손님') {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 3. 제목을 받아 { title: 제목, done: false } 객체를 돌려주세요.
export function makeTodo(title) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 4. 함수 fn과 값 value를 받아, fn을 두 번 적용한 결과를 돌려주세요.
//         예) applyTwice(n => n + 1, 5) → 7
export function applyTwice(fn, value) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 5. 버튼 객체를 만들어 돌려주세요.
//         { label: 버튼글자, click: 함수 } 이고, click()을 부르면 onClick(label)이 실행되어야 합니다.
export function createButton(label, onClick) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 6. 제목 검증 함수 (early return 사용)
//         공백뿐이면 '제목을 입력하세요.', 앞뒤 공백을 뺀 길이가 20자를 넘으면 '20자 이하로 입력하세요.',
//         통과하면 null을 돌려주세요.
export function validateTitle(title) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 7. 할 일 id를 받아 "삭제 버튼을 눌렀을 때 실행할 함수"를 돌려주세요.
//         돌려준 함수를 실행하면 onDelete(id)가 불려야 합니다.
//         React의 onClick={() => onDelete(todo.id)} 와 같은 원리입니다.
export function makeDeleteHandler(id, onDelete) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

check('1. 제곱', () => square(4), 16);
check('2. 기본값', () => [greet(), greet('민수')], ['손님님 환영합니다', '민수님 환영합니다']);
check('3. 할 일 객체', () => makeTodo('공부'), { title: '공부', done: false });
check('4. 두 번 적용', () => applyTwice(n => n * 3, 2), 18);
check('5. 버튼 클릭', () => {
  let clicked = null;
  const button = createButton('저장', label => (clicked = label));
  button.click();
  return [button.label, clicked];
}, ['저장', '저장']);
check('6. 제목 검증', () => [validateTitle('  '), validateTitle('a'.repeat(21)), validateTitle(' 공부 ')], ['제목을 입력하세요.', '20자 이하로 입력하세요.', null]);
check('7. 삭제 핸들러', () => {
  const deleted = [];
  const handler = makeDeleteHandler(7, id => deleted.push(id));
  const beforeClick = deleted.length; // 만들기만 했을 때는 실행되면 안 된다
  handler();
  return [beforeClick, deleted];
}, [0, [7]]);
summary();
