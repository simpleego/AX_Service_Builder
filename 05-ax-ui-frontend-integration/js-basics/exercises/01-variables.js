// ============================================================
// 연습 01. 변수와 자료형
// 실행: node exercises/01-variables.js   (정답: solutions/01-variables.js)
// ▼ 와 ▲ 사이에 코드를 작성하고 다시 실행해 보세요. 모두 ✅ 가 되면 통과입니다.
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 이름을 받아 "안녕하세요, 민수님!" 형태의 문자열을 돌려주세요. (템플릿 리터럴 사용)
export function makeGreeting(name) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 2. 숫자를 받아 "3개 남음" 형태의 문자열을 돌려주세요.
export function countLabel(count) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 3. 입력값의 앞뒤 공백을 지운 문자열을 돌려주세요.
export function cleanTitle(text) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 4. 앞뒤 공백을 지운 뒤의 글자 수를 돌려주세요.
export function titleLength(text) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 5. 문자열 '42'를 숫자 42로 바꿔 돌려주세요.
export function toNumber(text) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 6. 주소에서 받은 id 문자열이 "1 이상의 정수"인지 true/false로 돌려주세요.
//         힌트: Number(), Number.isInteger()
export function isValidId(text) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 7. 'YYYY-MM-DD' 형태의 날짜에서 연도 4글자만 잘라 돌려주세요. (slice)
export function getYear(date) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

check('1. 인사말', () => makeGreeting('민수'), '안녕하세요, 민수님!');
check('2. 남은 개수', () => countLabel(3), '3개 남음');
check('3. 공백 지우기', () => cleanTitle('  React 공부  '), 'React 공부');
check('4. 글자 수', () => titleLength('  abc  '), 3);
check('5. 숫자로 바꾸기', () => toNumber('42') + 1, 43);
check('6-1. 올바른 id', () => isValidId('3'), true);
check('6-2. 문자 id', () => isValidId('abc'), false);
check('6-3. 0과 소수', () => [isValidId('0'), isValidId('1.5')], [false, false]);
check('7. 연도', () => getYear('2026-10-21'), '2026');
summary();
