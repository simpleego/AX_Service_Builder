// ============================================================
// 연습 05. 배열과 배열 메서드
// 실행: node exercises/05-arrays.js   (정답: solutions/05-arrays.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요. for 문 대신 map/filter/find 등을 써 보세요.
// ============================================================
import { check, summary } from '../lib/check.js';

const todos = [
  { id: 1, title: '장보기', done: false, price: 12000 },
  { id: 2, title: 'React 공부', done: true, price: 0 },
  { id: 3, title: '운동하기', done: false, price: 5000 },
];

// 문제 1. 제목만 모은 배열을 돌려주세요. (map)
export function getTitles(list) {
  // ▼
  return list.map(t => t.title);
  // ▲
}

// 문제 2. 완료되지 않은 항목만 돌려주세요. (filter)
export function getActive(list) {
  // ▼
  return list.filter(t => !t.done);
  // ▲
}

// 문제 3. id가 같은 항목 하나를 돌려주세요. 없으면 undefined. (find)
export function findById(list, id) {
  // ▼
  return list.find(t => t.id === id);
  // ▲
}

// 문제 4. 완료된 항목의 개수를 돌려주세요.
export function countDone(list) {
  // ▼
  return list.filter(t => t.done).length;
  // ▲
}

// 문제 5. 하나라도 완료된 항목이 있으면 true. (some)
export function hasDone(list) {
  // ▼
  return list.some(t => t.done);
  // ▲
}

// 문제 6. 제목에 keyword가 들어간 항목만 돌려주세요. 대소문자는 구분하지 않습니다.
export function searchByTitle(list, keyword) {
  // ▼
  const q = keyword.toLowerCase();
  return list.filter(t => t.title.toLowerCase().includes(q));
  // ▲
}

// 문제 7. price의 합계를 돌려주세요. (reduce 또는 다른 방법)
export function totalPrice(list) {
  // ▼
  return list.reduce((sum, t) => sum + t.price, 0);
  // ▲
}

// 문제 8. 제목 가나다순으로 정렬한 "새 배열"을 돌려주세요. 원본 순서는 바뀌면 안 됩니다.
//         힌트: [...list].sort((a, b) => a.title.localeCompare(b.title, 'ko'))
//         'ko'는 한국어 기준 정렬이라는 뜻입니다. 이 기준에서는 한글이 영어보다 앞에 옵니다.
//         (빼면 컴퓨터의 언어 설정에 따라 결과가 달라질 수 있습니다)
export function sortByTitle(list) {
  // ▼
  return [...list].sort((a, b) => a.title.localeCompare(b.title, 'ko'));
  // ▲
}

// 문제 9. [값, 함수] 모양의 배열을 받아, 배열 구조 분해로 꺼낸 뒤 함수(값)의 결과를 돌려주세요.
//         예) useResult([3, n => n * 2]) → 6   (React의 const [count, setCount] = useState(0) 모양)
export function useResult(pair) {
  // ▼
  const [value, fn] = pair;
  return fn(value);
  // ▲
}

check('1. 제목 목록', () => getTitles(todos), ['장보기', 'React 공부', '운동하기']);
check('2. 진행 중', () => getActive(todos).map(t => t.id), [1, 3]);
check('3-1. 찾기', () => findById(todos, 2)?.title, 'React 공부');
check('3-2. 없는 id는 undefined', () => [findById(todos, 3)?.id, findById(todos, 99)], [3, undefined]);
check('4. 완료 개수', () => countDone(todos), 1);
check('5. 완료 있음?', () => [hasDone(todos), hasDone(getActive(todos))], [true, false]);
check('6. 검색 (대소문자 무시)', () => getTitles(searchByTitle(todos, 'react')), ['React 공부']);
check('7. 합계', () => totalPrice(todos), 17000);
check('8-1. 정렬 (한국어 기준)', () => getTitles(sortByTitle(todos)), ['운동하기', '장보기', 'React 공부']);
check('8-2. 원본 순서 유지', () => {
  const sorted = sortByTitle(todos);
  return [sorted?.length, todos.map(t => t.id)];
}, [3, [1, 2, 3]]);
check('9. 배열 구조 분해', () => useResult([3, n => n * 2]), 6);
summary();
