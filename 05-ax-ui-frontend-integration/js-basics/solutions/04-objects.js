// ============================================================
// 연습 04. 객체
// 실행: node exercises/04-objects.js   (정답: solutions/04-objects.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// ============================================================
import { check, summary } from '../lib/check.js';

// 문제 1. 구조 분해로 title만 꺼내 돌려주세요.
export function getTitle(todo) {
  // ▼
  const { title } = todo;
  return title;
  // ▲
}

// 문제 2. "공부 / 완료 / 메모없음" 형태로 돌려주세요.
//         memo가 없으면 '메모없음'을 쓰세요. (구조 분해 기본값 활용)
export function describeTodo(todo) {
  // ▼
  const { title, done, memo = '메모없음' } = todo;
  return `${title} / ${done ? '완료' : '진행 중'} / ${memo}`;
  // ▲
}

// 문제 3. done만 true로 바꾼 "새 객체"를 돌려주세요. 원본은 바뀌면 안 됩니다.
export function completeTodo(todo) {
  // ▼
  return { ...todo, done: true };
  // ▲
}

// 문제 4. form 객체에서 name에 해당하는 칸만 value로 바꾼 새 객체를 돌려주세요.
//         예) updateField({ title: '', priority: 'low' }, 'title', '공부') → { title: '공부', priority: 'low' }
export function updateField(form, name, value) {
  // ▼
  return { ...form, [name]: value };
  // ▲
}

// 문제 5. 기본값 { priority: 'medium', memo: '' } 위에 input을 덮어쓴 새 객체를 돌려주세요.
export function withDefaults(input) {
  // ▼
  return { priority: 'medium', memo: '', ...input };
  // ▲
}

// 문제 6. 에러 객체의 키 개수를 돌려주세요. 예) { title: '…', memo: '…' } → 2
export function countErrors(errors) {
  // ▼
  return Object.keys(errors).length;
  // ▲
}

// 문제 7. { high: '높음', low: '낮음' } 을 [{ value: 'high', label: '높음' }, { value: 'low', label: '낮음' }] 로 바꿔 주세요.
//         (React에서 <select>의 <option> 목록을 만들 때 쓰는 모양)
export function toOptions(labels) {
  // ▼
  return Object.entries(labels).map(([value, label]) => ({ value, label }));
  // ▲
}

const sample = { id: 1, title: '공부', done: false };
check('1. 제목 꺼내기', () => getTitle(sample), '공부');
check('2-1. 설명 (메모 없음)', () => describeTodo(sample), '공부 / 진행 중 / 메모없음');
check('2-2. 설명 (메모 있음)', () => describeTodo({ title: '운동', done: true, memo: '30분' }), '운동 / 완료 / 30분');
check('3-1. 완료로 바꾸기', () => completeTodo(sample), { id: 1, title: '공부', done: true });
check('3-2. 원본은 그대로', () => {
  const original = { id: 2, title: 'A', done: false };
  const result = completeTodo(original);
  return [original.done, result?.done];
}, [false, true]);
check('4. 칸 하나 바꾸기', () => updateField({ title: '', priority: 'low' }, 'title', '공부'), { title: '공부', priority: 'low' });
check('5. 기본값 합치기', () => withDefaults({ title: '새 일', priority: 'high' }), { priority: 'high', memo: '', title: '새 일' });
check('6. 에러 개수', () => [countErrors({}), countErrors({ title: 'x', memo: 'y' })], [0, 2]);
check('7. 옵션 목록', () => toOptions({ high: '높음', low: '낮음' }), [{ value: 'high', label: '높음' }, { value: 'low', label: '낮음' }]);
summary();
