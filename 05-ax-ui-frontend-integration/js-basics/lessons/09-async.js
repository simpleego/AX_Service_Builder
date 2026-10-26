// ============================================================
// 09. 비동기: setTimeout, Promise, async/await, 에러 처리
// 실행: node lessons/09-async.js
// ============================================================
// 서버에 데이터를 요청하면 응답이 올 때까지 시간이 걸립니다.
// 그동안 화면이 멈추면 안 되므로, "기다리는 일"은 비동기로 처리합니다.
// 이 단원은 진짜 서버 대신 "가짜 서버"로 연습합니다. (인터넷 연결 불필요)

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

// 가짜 서버 데이터
const DB = [
  { id: 1, title: '장보기', done: false },
  { id: 2, title: 'React 공부', done: true },
];

// ── 가짜 fetch: 진짜 fetch와 같은 모양의 응답을 돌려준다 ─────
// 진짜 fetch도 Promise를 돌려주고, 응답에는 ok, status, json() 이 있다.
async function fakeFetch(url) {
  await wait(100); // 네트워크가 걸리는 시간 흉내
  if (url === '/down') throw new TypeError('Failed to fetch'); // 서버가 꺼진 경우

  // **“문자열이 /todos/로 시작하고, 그 뒤에 숫자가 한 개 이상 나오며, 숫자로 끝나야 한다”
  const match = url.match(/^\/todos\/(\d+)$/);
  if (url === '/todos') return { ok: true, status: 200, json: async () => DB };
  if (match) {
    const todo = DB.find(t => t.id === Number(match[1]));
    if (todo) return { ok: true, status: 200, json: async () => todo };
  }
  return { ok: false, status: 404, json: async () => ({ message: 'Not Found' }) };
}

async function main() {
  // ── 1. 실행 순서 ──────────────────────────────────────────
  console.log('[1] 실행 순서');
  console.log('  A. 요청 보냄');
  setTimeout(() => console.log('  C. 응답 도착 (0.05초 뒤)'), 50);
  console.log('  B. 기다리는 동안 다른 일 계속');
  await wait(60); // (다음 예제가 섞이지 않도록 잠시 기다림)

  // ── 2. Promise: "나중에 값을 주겠다는 약속" ───────────────
  // 상태: 기다리는 중(pending) → 성공(fulfilled) 또는 실패(rejected)
  console.log('\n[2] Promise와 then/catch');
  const promise = fakeFetch('/todos');
  console.log('  바로 찍으면:', promise instanceof Promise ? 'Promise { <pending> }' : promise);
  await promise
    .then(res => res.json())
    .then(data => console.log('  then으로 받은 개수:', data.length)) // 2
    .catch(err => console.log('  실패:', err.message));

  // ── 3. async / await: Promise를 위에서 아래로 읽히게 쓰기 ──
  // async 함수 안에서 await 를 쓰면 결과가 올 때까지 "그 함수만" 기다린다.
  console.log('\n[3] async/await');
  const res = await fakeFetch('/todos/2');
  const todo = await res.json();
  console.log('  ', todo.title); // React 공부

  // ── 4. 에러 처리: try / catch / finally ─────────────────
  // React 화면의 "로딩 중 → 성공 또는 에러" 흐름을 그대로 흉내 낸다.
  console.log('\n[4] 로딩 / 성공 / 에러 상태 흉내');
  async function loadTodo(url) {
    const state = { loading: true, data: null, error: null };
    try {
      const res = await fakeFetch(url);
      // [중요] fetch는 404·500이어도 에러를 던지지 않는다. 직접 확인해야 한다.
      if (!res.ok) throw new Error(`요청 실패 (${res.status})`);
      state.data = await res.json();
    } catch (error) {
      state.error = error.message;
    } finally {
      state.loading = false; // 성공이든 실패든 로딩은 끝난다
    }
    return state;
  }
  console.log('  ', JSON.stringify(await loadTodo('/todos/1')));  // {"loading":false,"data":{"id":1,…},"error":null}
  console.log('  ', JSON.stringify(await loadTodo('/todos/99'))); // {"loading":false,"data":null,"error":"요청 실패 (404)"}
  console.log('  ', JSON.stringify(await loadTodo('/down')));     // {"loading":false,"data":null,"error":"Failed to fetch"}

  // ── 5. 여러 요청을 동시에: Promise.all ──────────────────
  console.log('\n[5] 순서대로 vs 동시에');
  let start = Date.now();
  await fakeFetch('/todos/1');
  await fakeFetch('/todos/2');
  console.log(`  순서대로 두 번: 약 ${Math.round((Date.now() - start) / 100) * 100}ms`); // 약 200ms

  start = Date.now();
  const results = await Promise.all([fakeFetch('/todos/1'), fakeFetch('/todos/2')]);
  console.log(`  Promise.all:    약 ${Math.round((Date.now() - start) / 100) * 100}ms, 결과 ${results.length}개`); // 약 100ms

  // ── 6. 에러 직접 만들기 ─────────────────────────────────
  // throw 로 에러를 던지면, 가장 가까운 catch 가 받는다.
  // 상태 코드 같은 정보를 더 담고 싶으면 Error를 확장한 클래스를 만든다.
  class ApiError extends Error {
    constructor(status, message) {
      super(message);
      this.status = status;
    }
  }
  console.log('\n[6] 에러 클래스');
  try {
    throw new ApiError(404, '없는 할 일입니다.');
  } catch (error) {
    console.log(`  ${error.status}: ${error.message}`); // 404: 없는 할 일입니다.
    console.log('  ApiError인가?', error instanceof ApiError); // true
  }

  // ── 7. 자주 하는 실수: await 를 빠뜨림 ──────────────────
  console.log('\n[7] await 를 빠뜨리면');
  const forgot = fakeFetch('/todos');
  console.log('  forgot.ok =', forgot.ok); // undefined ← 응답이 아니라 Promise를 들고 있다
  await forgot; // (정리)
}

main();

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// v2 api/client.ts:  const res = await fetch(url); if (!res.ok) throw new ApiError(...)
// v2 TodoForm:       try { await onSubmit(values); } catch { /* 입력값 유지 */ }
// v2 useTodos:       Promise.all(ids.map(id => deleteTodo(id)))
// 화면 상태:         isPending → 로딩, isError → 에러, data → 목록
// ============================================================

추가적인 주석을 달아줘
