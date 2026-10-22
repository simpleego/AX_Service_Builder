// ============================================================
// 연습 06. 참조와 불변성
// 실행: node exercises/06-immutability.js   (정답: solutions/06-immutability.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// 모든 문제의 공통 규칙: 받은 배열·객체를 절대 직접 고치지 말고, 새로 만들어 돌려주세요.
// (push, splice, sort, 직접 대입 금지)
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 배열 끝에 item을 추가한 새 배열
export function addItem(list, item) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 2. 배열 맨 앞에 item을 추가한 새 배열 (최신 항목을 위에 보여 줄 때)
export function prependItem(list, item) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 3. id가 같은 항목을 뺀 새 배열
export function removeById(list, id) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 4. id가 같은 항목의 done을 반대로 바꾼 새 배열
export function toggleById(list, id) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 5. id가 같은 항목에 patch 객체의 내용을 덮어쓴 새 배열
//         예) updateById(list, 1, { title: '새 제목', done: true })
export function updateById(list, id, patch) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 6. user.settings.theme 만 바꾼 새 user 객체 (안쪽 객체도 새로 만들어야 함)
export function changeTheme(user, theme) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 7. React가 "다시 그릴지" 판단하는 방식 흉내: 이전 값과 새 값이 다른 상자면 true
export function willRerender(prev, next) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// ── 채점 ─────────────────────────────────────────────────────
// 원본이 바뀌었는지 확인하기 위해 매번 새 데이터를 만든다
const make = () => [
  { id: 1, title: 'A', done: false },
  { id: 2, title: 'B', done: true },
];

/** 작업 후 결과와 "원본이 그대로인지"를 함께 확인 */
function result(fn) {
  const list = make();
  const snapshot = JSON.stringify(list);
  const out = fn(list);
  return { out, originalKept: JSON.stringify(list) === snapshot, isNew: out !== list };
}

check('1. 끝에 추가', () => {
  const r = result(l => addItem(l, { id: 3, title: 'C', done: false }));
  return [r.out.map(t => t.id), r.originalKept, r.isNew];
}, [[1, 2, 3], true, true]);
check('2. 앞에 추가', () => {
  const r = result(l => prependItem(l, { id: 0, title: 'Z', done: false }));
  return [r.out.map(t => t.id), r.originalKept];
}, [[0, 1, 2], true]);
check('3. 삭제', () => {
  const r = result(l => removeById(l, 1));
  return [r.out.map(t => t.id), r.originalKept];
}, [[2], true]);
check('4. 토글', () => {
  const r = result(l => toggleById(l, 1));
  return [r.out.map(t => t.done), r.originalKept, r.isNew];
}, [[true, true], true, true]);
check('5. 일부 수정', () => {
  const r = result(l => updateById(l, 2, { title: 'B2', done: false }));
  return [r.out[1], r.originalKept];
}, [{ id: 2, title: 'B2', done: false }, true]);
check('6. 안쪽 객체 수정', () => {
  const user = { name: '민수', settings: { theme: 'light', lang: 'ko' } };
  const next = changeTheme(user, 'dark');
  return [next.settings, user.settings.theme, next.settings !== user.settings];
}, [{ theme: 'dark', lang: 'ko' }, 'light', true]);
check('7. 다시 그릴까?', () => {
  const list = make();
  list[0].done = true; // 직접 수정
  return [willRerender(list, list), willRerender(list, [...list])];
}, [false, true]);
summary();
