// ============================================================
// 연습 09. 비동기와 에러 처리
// 실행: node exercises/09-async.js   (정답: solutions/09-async.js)
// ▼ 와 ▲ 사이에 코드를 작성하세요.
// 아래 fakeFetch는 진짜 fetch와 같은 모양으로 동작하는 가짜 서버입니다. (고치지 마세요)
// ============================================================
import { checkAsync, check, summary } from '../lib/check.js';

const wait = ms => new Promise(resolve => setTimeout(resolve, ms));
const DB = [
  { id: 1, title: '장보기' },
  { id: 2, title: 'React 공부' },
  { id: 3, title: '운동하기' },
];
async function fakeFetch(url) {
  await wait(30);
  if (url === '/down') throw new TypeError('Failed to fetch');
  const match = url.match(/^\/todos\/(\d+)$/);
  const todo = match && DB.find(t => t.id === Number(match[1]));
  if (todo) return { ok: true, status: 200, json: async () => todo };
  return { ok: false, status: 404, json: async () => ({}) };
}

// 문제 1. fakeFetch(`/todos/${id}`)로 할 일을 받아 제목을 돌려주세요.
//         응답이 실패(res.ok가 false)면 null을 돌려주세요.
export async function fetchTitle(id) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 2. 화면 상태 객체 { loading, data, error } 를 돌려주세요.
//         - 성공: { loading: false, data: 받은 할 일, error: null }
//         - res.ok가 false: { loading: false, data: null, error: '요청 실패 (404)' }
//         - fakeFetch가 에러를 던짐: { loading: false, data: null, error: 에러의 message }
//         힌트: try / catch / finally, throw new Error(...)
export async function loadState(url) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 3. 여러 id의 제목을 "동시에" 받아 배열로 돌려주세요. (Promise.all + 문제 1의 fetchTitle)
export async function fetchTitles(ids) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 4. fn()을 실행하고, 에러가 나면 한 번만 다시 시도하세요. 두 번째도 실패하면 에러를 그대로 던집니다.
//         fn은 Promise를 돌려주는 함수입니다.
export async function retryOnce(fn) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

// 문제 5. JSON 문자열을 객체로 바꿔 돌려주세요. 잘못된 문자열이면 에러 대신 null을 돌려주세요.
//         (localStorage에 저장된 값이 깨졌을 때 앱이 멈추지 않게 하는 방법)
export function parseJsonSafe(text) {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

await checkAsync('1-1. 제목 받기', () => fetchTitle(2), 'React 공부');
await checkAsync('1-2. 없는 id는 null', () => fetchTitle(99), null);
await checkAsync('2-1. 성공 상태', () => loadState('/todos/1'), { loading: false, data: { id: 1, title: '장보기' }, error: null });
await checkAsync('2-2. 404 상태', () => loadState('/todos/99'), { loading: false, data: null, error: '요청 실패 (404)' });
await checkAsync('2-3. 서버 꺼짐', () => loadState('/down'), { loading: false, data: null, error: 'Failed to fetch' });
await checkAsync('3-1. 여러 개 동시에', () => fetchTitles([3, 1]), ['운동하기', '장보기']);
await checkAsync('3-2. 정말 동시에? (순서대로면 약 90ms, 동시에면 약 30ms)', async () => {
  const start = Date.now();
  const titles = await fetchTitles([1, 2, 3]);
  return [titles, Date.now() - start < 70];
}, [['장보기', 'React 공부', '운동하기'], true]);
await checkAsync('4-1. 한 번 실패 후 성공', async () => {
  let tries = 0;
  const flaky = async () => {
    tries++;
    if (tries === 1) throw new Error('일시 오류');
    return '성공';
  };
  return [await retryOnce(flaky), tries];
}, ['성공', 2]);
await checkAsync('4-2. 두 번 다 실패하면 에러', async () => {
  try {
    await retryOnce(async () => {
      throw new Error('계속 실패');
    });
    return '에러가 나야 합니다';
  } catch (error) {
    return error.message;
  }
}, '계속 실패');
check('5. 안전한 JSON 읽기', () => [parseJsonSafe('{"a":1}'), parseJsonSafe('{')], [{ a: 1 }, null]);
summary();
