// ============================================================
// 07. 스코프와 클로저 (useState가 왜 그렇게 동작하는지)
// 실행: node lessons/07-scope-closure.js
// ============================================================
// "버튼을 세 번 눌렀는데 왜 1만 올라가지?" 같은 React 질문은
// 대부분 이 단원의 내용으로 설명됩니다.

// ── 1. 스코프: 변수가 보이는 범위 ───────────────────────────
// { } 안에서 만든 let/const 는 그 안에서만 보인다.
const appName = '할 일 앱'; // 바깥(전역) 변수: 어디서나 보인다
function showTitle() {
  const title = '목록'; // 함수 안 변수: 이 함수 안에서만 보인다
  return `${appName} - ${title}`;
}
console.log('[1] 스코프:', showTitle()); // 할 일 앱 - 목록
// console.log(title); // ← 에러: title은 함수 밖에서 보이지 않는다

if (true) {
  const inside = '블록 안';
  console.log(inside); // 블록 안
}
// console.log(inside); // ← 에러

// ── 2. 클로저: 함수는 자기가 "만들어질 때" 주변 변수를 기억한다 ─
function createCounter() {
  let count = 0; // 바깥에서는 직접 접근할 수 없는 값
  return {
    increase: () => {
      count = count + 1;
      return count;
    },
    get: () => count,
  };
}
const counterA = createCounter();
const counterB = createCounter(); // 따로 만들면 따로 기억한다
counterA.increase();
counterA.increase();
counterB.increase();
console.log('\n[2] 클로저:', counterA.get(), counterB.get()); // 2 1

// ── 3. 함수는 "그때의 값"을 본다 ────────────────────────────
let price = 1000;
const printLater = () => console.log(`    나중에 읽은 가격: ${price}`);
const savedPrice = price;
const printSaved = () => console.log(`    저장해 둔 가격: ${savedPrice}`);
price = 2000;
console.log('\n[3] 나중에 실행되는 함수');
setTimeout(() => {
  printLater(); // 2000 ← 변수 price를 기억하므로 바뀐 값이 보인다
  printSaved(); // 1000 ← 만들 때 따로 저장한 값
}, 10);

// ── 4. React의 state 업데이트 흉내 내기 ─────────────────────
// React에서 한 번의 렌더링 동안 state 변수(count)는 "고정된 값"이다.
// setCount를 불러도 지금 함수 안의 count는 바뀌지 않고, 다음 렌더링 때 바뀐다.
function createFakeState(initial) {
  let state = initial;
  let queue = [];
  return {
    current: () => state,
    setState: next => queue.push(next), // 바로 바꾸지 않고 "예약"만 한다
    rerender: () => {
      for (const next of queue) {
        // 함수를 넘기면 "직전 값"을 받아 계산한다
        state = typeof next === 'function' ? next(state) : next;
      }
      queue = [];
      return state;
    },
  };
}

setTimeout(() => {
  console.log('\n[4] state 업데이트 흉내');

  const s1 = createFakeState(0);
  const count = s1.current(); // 이번 렌더링의 count는 0으로 고정
  s1.setState(count + 1); // 0 + 1
  s1.setState(count + 1); // 0 + 1 (count는 여전히 0!)
  s1.setState(count + 1); // 0 + 1
  console.log('    setCount(count + 1) 세 번 →', s1.rerender()); // 1

  const s2 = createFakeState(0);
  s2.setState(prev => prev + 1); // 0 → 1
  s2.setState(prev => prev + 1); // 1 → 2
  s2.setState(prev => prev + 1); // 2 → 3
  console.log('    setCount(prev => prev + 1) 세 번 →', s2.rerender()); // 3
  console.log('    → 이전 값을 기준으로 바꿀 때는 함수 형태로 넘긴다');
}, 20);

// ── 5. 정리(cleanup) 함수가 필요한 이유 ─────────────────────
// 타이머를 만들고 취소하지 않으면, 필요 없어진 뒤에도 계속 실행된다.
setTimeout(() => {
  console.log('\n[5] 타이머 취소 (디바운스의 원리)');
  let timer;
  function onType(text) {
    clearTimeout(timer); // 이전 예약을 취소
    timer = setTimeout(() => console.log(`    검색 요청: "${text}"`), 50);
  }
  onType('r');
  onType('re');
  onType('rea');
  onType('react'); // 마지막 것만 실행된다 → 검색 요청: "react"
}, 30);

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// 이전 값 기준 업데이트: setValues(prev => ({ ...prev, [name]: value }))   (v2 TodoForm)
// 커스텀 훅 = 클로저:    useDebounce가 timer를 기억하고 정리 함수에서 취소
// 정리 함수:             useEffect(() => { const t = setTimeout(…); return () => clearTimeout(t); }, [value])
// ============================================================
