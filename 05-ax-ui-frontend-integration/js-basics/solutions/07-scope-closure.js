// ============================================================
// 연습 07. 스코프와 클로저
// 실행: node exercises/07-scope-closure.js   (정답: solutions/07-scope-closure.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// ============================================================
import { check, checkAsync, summary } from '../lib/check.js';

// 문제 1. 카운터를 만들어 돌려주세요.
//         increase()는 1 올리고, decrease()는 1 내리고, get()은 현재 값을 돌려줍니다. 처음 값은 start.
export function createCounter(start = 0) {
  // ▼
  let count = start;
  return {
    increase: () => (count += 1),
    decrease: () => (count -= 1),
    get: () => count,
  };
  // ▲
}

// 문제 2. 부를 때마다 1, 2, 3 … 순서대로 새 id를 돌려주는 "함수"를 돌려주세요.
//         예) const nextId = createIdGenerator(); nextId() → 1, nextId() → 2
export function createIdGenerator() {
  // ▼
  let last = 0;
  return () => {
    last += 1;
    return last;
  };
  // ▲
}

// 문제 3. React의 state 업데이트 흉내.
//         updates 배열을 앞에서부터 적용한 최종 값을 돌려주세요.
//         항목이 함수면 "직전 값"을 넣어 실행한 결과로, 함수가 아니면 그 값으로 바꿉니다.
//         예) applyUpdates(0, [5, prev => prev * 2]) → 10
export function applyUpdates(initial, updates) {
  // ▼
  let state = initial;
  for (const next of updates) {
    state = typeof next === 'function' ? next(state) : next;
  }
  return state;
  // ▲
}

// 문제 4. fn을 "처음 한 번만" 실행하는 함수를 돌려주세요.
//         두 번째부터는 fn을 실행하지 않고 처음 결과를 그대로 돌려줍니다.
export function once(fn) {
  // ▼
  let called = false;
  let result;
  return (...args) => {
    if (!called) {
      called = true;
      result = fn(...args);
    }
    return result;
  };
  // ▲
}

// 문제 5. 디바운스: 연속으로 불리면 마지막 호출만, ms 밀리초 뒤에 fn(값)을 실행하는 함수를 돌려주세요.
//         힌트: 바깥에 timer 변수를 두고, 부를 때마다 clearTimeout 후 setTimeout
export function debounce(fn, ms) {
  // ▼
  let timer;
  return value => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(value), ms);
  };
  // ▲
}

check('1. 카운터', () => {
  const c = createCounter(10);
  c.increase();
  c.increase();
  c.decrease();
  return c.get();
}, 11);
check('1-2. 카운터는 서로 독립', () => {
  const a = createCounter();
  const b = createCounter();
  a.increase();
  return [a.get(), b.get()];
}, [1, 0]);
check('2. id 생성기', () => {
  const nextId = createIdGenerator();
  return [nextId(), nextId(), nextId()];
}, [1, 2, 3]);
check('3-1. 값으로 세 번 (React의 count + 1 세 번)', () => applyUpdates(0, [1, 1, 1]), 1);
check('3-2. 함수로 세 번 (prev => prev + 1 세 번)', () => applyUpdates(0, [p => p + 1, p => p + 1, p => p + 1]), 3);
check('3-3. 섞어서', () => applyUpdates(0, [5, p => p * 2]), 10);
check('4. 한 번만 실행', () => {
  let calls = 0;
  const init = once(() => ++calls * 100);
  return [init(), init(), calls];
}, [100, 100, 1]);
await checkAsync('5. 디바운스', async () => {
  const sent = [];
  const search = debounce(q => sent.push(q), 30);
  search('r');
  search('re');
  search('react');
  await new Promise(r => setTimeout(r, 80));
  return sent;
}, ['react']);
summary();
