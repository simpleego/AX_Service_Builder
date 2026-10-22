// ============================================================
// 연습 02. 비교, 논리 연산자, 조건문
// 실행: node exercises/02-conditions.js   (정답: solutions/02-conditions.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 점수가 90 이상이면 'A', 80 이상이면 'B', 나머지는 'C'를 돌려주세요.
export function gradeOf(score) {
  // ▼
  if (score >= 90) return 'A';
  if (score >= 80) return 'B';
  return 'C';
  // ▲
}

// 문제 2. done이 true면 '완료', false면 '진행 중'을 돌려주세요. (삼항 연산자 한 줄로)
export function statusLabel(done) {
  // ▼
  return done ? '완료' : '진행 중';
  // ▲
}

// 문제 3. 배열이 비어 있으면 true를 돌려주세요. (빈 배열은 truthy라는 점에 주의)
export function isEmpty(list) {
  // ▼
  return list.length === 0;
  // ▲
}

// 문제 4. React에서 "개수가 있을 때만 배지 보여 주기"를 흉내 냅니다.
//         count가 0보다 크면 "3개" 같은 문자열을, 아니면 false를 돌려주세요.
//         (count && ... 로 쓰면 0이 그대로 나오는 버그가 생깁니다)
export function badge(count) {
  // ▼
  return count > 0 && `${count}개`;
  // ▲
}

// 문제 5. value가 null 또는 undefined일 때만 '기본값'을 돌려주고, 나머지는 그대로 돌려주세요.
export function withDefault(value) {
  // ▼
  return value ?? '기본값';
  // ▲
}

// 문제 6. user가 없거나 이름이 없으면 '손님', 있으면 그 이름을 돌려주세요. (?. 와 ?? 사용)
export function userName(user) {
  // ▼
  return user?.name ?? '손님';
  // ▲
}

// 문제 7. 할 일이 "기한 지남"인지 돌려주세요.
//         조건: 완료되지 않았고, 마감일('YYYY-MM-DD')이 비어 있지 않고, 마감일이 today보다 이전
export function isOverdue(todo, today) {
  // ▼
  return !todo.done && todo.dueDate !== '' && todo.dueDate < today;
  // ▲
}

check('1. 학점', () => [gradeOf(95), gradeOf(85), gradeOf(50)], ['A', 'B', 'C']);
check('2. 상태 글자', () => [statusLabel(true), statusLabel(false)], ['완료', '진행 중']);
check('3. 빈 배열', () => [isEmpty([]), isEmpty([1])], [true, false]);
check('4-1. 배지 있음', () => badge(3), '3개');
check('4-2. 배지 없음 (0이 나오면 안 됨)', () => badge(0), false);
check('5. ?? 기본값', () => [withDefault(null), withDefault(undefined), withDefault(0), withDefault('')], ['기본값', '기본값', 0, '']);
check('6. 사용자 이름', () => [userName(null), userName({}), userName({ name: '민수' })], ['손님', '손님', '민수']);
check('7-1. 기한 지남', () => isOverdue({ done: false, dueDate: '2026-10-01' }, '2026-10-21'), true);
check('7-2. 완료한 일은 아님', () => isOverdue({ done: true, dueDate: '2026-10-01' }, '2026-10-21'), false);
check('7-3. 마감일 없음', () => isOverdue({ done: false, dueDate: '' }, '2026-10-21'), false);
summary();
