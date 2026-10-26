// ============================================================
// 09. 비동기: setTimeout, Promise, async/await, 에러 처리
// 실행: node lessons/09-async.js
// ============================================================
//
// [비동기가 필요한 이유]
// 서버에 데이터를 요청하면 응답이 올 때까지 시간이 걸립니다.
// 이때 JavaScript가 아무 일도 하지 못하고 기다리면 불편합니다.
//
// 비동기는 시간이 걸리는 작업을 시작한 뒤,
// 그 작업이 완료되기를 기다리는 동안 다른 작업을 처리하는 방식입니다.
//
// 예: 서버에서 할 일 목록을 가져오는 동안에도
//     사용자는 버튼을 누르거나 입력창에 글을 입력할 수 있습니다.
//
// 주의: async를 붙인다고 복잡한 계산이 자동으로 별도 스레드에서
// 실행되는 것은 아닙니다. 긴 동기 계산은 여전히 실행을 막을 수 있습니다.
//
// 이 단원은 실제 서버 대신 "가짜 서버"로 연습합니다.
// 따라서 인터넷 연결 없이도 실행할 수 있습니다.


// ============================================================
// 준비 1. 일정 시간이 지난 뒤 완료되는 Promise 만들기
// ============================================================
//
// wait(100)은 "100ms 뒤에 완료되는 Promise"를 반환합니다.
// 1,000ms = 1초이므로 100ms는 0.1초입니다.
//
// new Promise(...) : 비동기 작업의 완료 또는 실패를 표현하는 객체 생성
// resolve          : Promise를 성공 상태로 바꾸는 함수
// setTimeout       : 지정한 시간이 지난 뒤 콜백 실행을 예약
//
// 여기서는 시간이 지나면 resolve()를 호출하여 성공으로 완료합니다.
// resolve에 값을 전달하지 않으므로 완료 결과는 undefined입니다.
//
// 참고: 타이머의 시간은 정확한 실행 시각을 보장하지 않습니다.
// 다른 작업이 실행 중이면 콜백 실행이 더 늦어질 수 있습니다.
const wait = ms => new Promise(resolve => setTimeout(resolve, ms));

// 위 코드를 일반 함수 형태로 풀어 쓰면 다음과 같습니다.
//
// function wait(ms) {
//   return new Promise(function (resolve) {
//     setTimeout(function () {
//       resolve();
//     }, ms);
//   });
// }
//
// 사용 예:
// await wait(100);
// → 현재 async 함수의 실행을 잠시 멈췄다가 약 100ms 후 이어서 실행


// ============================================================
// 준비 2. 가짜 서버 데이터
// ============================================================
//
// 실제 데이터베이스 대신 메모리에 있는 배열을 사용합니다.
// 프로그램을 종료하면 메모리에 있는 데이터는 사라집니다.
//
// id    : 할 일을 구분하는 고유 번호
// title : 할 일 제목
// done  : 완료 여부(true: 완료, false: 미완료)
const DB = [
  { id: 1, title: '장보기', done: false },
  { id: 2, title: 'React 공부', done: true },
];


// ============================================================
// 준비 3. 실제 fetch의 일부 동작을 흉내 내는 가짜 fetch
// ============================================================
//
// 실제 fetch(url)는 서버에 HTTP 요청을 보내고,
// 응답을 나타내는 Response 객체로 완료되는 Promise를 반환합니다.
//
// 여기서는 학습에 필요한 다음 항목만 구현합니다.
//
// ok     : 요청의 HTTP 상태가 성공 범위인지 여부
//          실제 Response에서는 상태 코드가 200~299이면 true
// status : HTTP 상태 코드(예: 200, 404)
// json() : 응답 본문을 JavaScript 값으로 읽는 비동기 메서드
//
// 주의: fakeFetch는 실제 네트워크 통신이나 JSON 파싱을 하지 않습니다.
// DB의 객체나 배열을 그대로 반환하는 학습용 구현입니다.
//
// async 함수는 항상 Promise를 반환합니다.
// - return 값  → 해당 값으로 Promise 성공
// - throw 에러 → 해당 에러로 Promise 실패
async function fakeFetch(url) {
  // 네트워크 요청과 응답에 시간이 걸리는 상황을 흉내 냅니다.
  // fakeFetch의 나머지 실행만 대기하며 전체 프로그램을 멈추지 않습니다.
  await wait(100);

  // 서버에 연결할 수 없는 네트워크 실패 상황을 흉내 냅니다.
  //
  // async 함수 안에서 throw가 실행되면 반환한 Promise가 rejected가 됩니다.
  // 호출한 쪽에서는 await + try/catch 또는 .catch()로 처리할 수 있습니다.
  //
  // 실제 fetch의 TypeError는 서버 중단 외에도 네트워크 장애,
  // 브라우저의 CORS 차단 등 여러 원인으로 발생할 수 있습니다.
  if (url === '/down') throw new TypeError('Failed to fetch');

  // "/todos/1", "/todos/2"처럼 번호가 붙은 주소인지 확인합니다.
  //
  // 정규식 /^\/todos\/(\d+)$/의 의미:
  // ^        : 문자열 시작
  // \/todos\/: "/todos/"라는 문자열
  // (\d+)    : 숫자 1개 이상을 찾고 괄호로 묶은 부분을 저장
  // $        : 문자열 끝
  //
  // "/todos/2"라면 match[1]은 문자열 "2"입니다.
  // 형식이 일치하지 않으면 match는 null입니다.
  const match = url.match(/^\/todos\/(\d+)$/);

  // 전체 목록을 요청한 경우: HTTP 200 성공 응답을 흉내 냅니다.
  //
  // json: async () => DB
  // → json이라는 이름의 메서드를 정의
  // → 호출하면 DB 배열로 완료되는 Promise를 반환
  //
  // 따라서 호출한 쪽에서는 await res.json()으로 배열을 꺼냅니다.
  if (url === '/todos') return { ok: true, status: 200, json: async () => DB };

  // 특정 번호의 할 일을 요청한 경우
  if (match) {
    // match[1]은 문자열이므로 Number()로 숫자로 변환합니다.
    //
    // find()는 조건에 맞는 첫 번째 요소를 반환합니다.
    // 조건에 맞는 요소가 없으면 undefined를 반환합니다.
    //
    // 예: "/todos/2" → DB에서 id === 2인 객체 검색
    const todo = DB.find(t => t.id === Number(match[1]));

    // 해당 할 일이 있으면 HTTP 200 성공 응답을 반환합니다.
    if (todo) return { ok: true, status: 200, json: async () => todo };
  }

  // 주소가 없거나 해당 번호의 할 일이 없으면 HTTP 404를 반환합니다.
  //
  // 중요: 여기서는 throw를 실행하지 않습니다.
  // Promise 자체는 성공하고, 응답 객체의 ok만 false가 됩니다.
  //
  // 즉, 다음 두 상황은 다릅니다.
  // - /down     : 응답을 받지 못함 → Promise 실패
  // - /todos/99 : 404 응답을 받음  → Promise 성공, res.ok는 false
  return { ok: false, status: 404, json: async () => ({ message: 'Not Found' }) };
}


// ============================================================
// 예제를 차례대로 실행하는 메인 함수
// ============================================================
//
// 내부에서 await를 사용하므로 async 함수로 선언합니다.
// main()도 호출하면 Promise를 반환합니다.
async function main() {
  // ── 1. 실행 순서 ──────────────────────────────────────────
  console.log('[1] 실행 순서');

  // 첫 번째: 즉시 실행됩니다.
  console.log('  A. 요청 보냄');

  // 콜백 실행을 예약하고 즉시 다음 줄로 넘어갑니다.
  // 여기서 50ms 동안 멈춰 있는 것이 아닙니다.
  //
  // () => console.log(...)는 나중에 실행할 콜백 함수입니다.
  // 이 예제의 "응답 도착"은 실제 응답이 아니라 타이머 출력입니다.
  setTimeout(() => console.log('  C. 응답 도착 (0.05초 뒤)'), 50);

  // 두 번째: 타이머 콜백을 기다리지 않고 즉시 실행됩니다.
  console.log('  B. 기다리는 동안 다른 일 계속');

  // 일반적인 출력 순서: A → B → C
  //
  // 다음 단원의 출력과 섞이지 않도록 main 함수만 잠시 대기합니다.
  // 대기하는 동안 예약된 타이머 콜백은 실행될 수 있습니다.
  await wait(60);


  // ── 2. Promise: "나중에 값을 주겠다는 약속" ───────────────
  //
  // Promise의 상태:
  // pending   : 결과를 기다리는 중
  // fulfilled : 성공적으로 완료됨
  // rejected  : 실패함
  //
  // 성공 또는 실패로 한 번 결정된 상태는 다시 바뀌지 않습니다.
  console.log('\n[2] Promise와 then/catch');

  // fakeFetch를 호출하면 작업이 시작되고 Promise가 즉시 반환됩니다.
  // 이 변수에는 아직 할 일 목록이나 응답 객체가 들어 있지 않습니다.
  const promise = fakeFetch('/todos');

  // instanceof Promise는 Promise 객체인지 확인하는 연산입니다.
  //
  // 주의: 이 코드는 실제 내부 상태를 읽는 것이 아니라
  // Promise이면 안내용 문자열 "Promise { <pending> }"를 출력합니다.
  // instanceof만으로 pending 상태인지 판단할 수는 없습니다.
  console.log('  바로 찍으면:', promise instanceof Promise ? 'Promise { <pending> }' : promise);

  // .then()  : Promise가 성공했을 때 실행할 함수 등록
  // .catch() : 앞선 Promise 체인에서 발생한 실패를 처리
  //
  // 흐름:
  // fakeFetch 완료
  // → 응답 객체 res 전달
  // → res.json() 호출
  // → 데이터 읽기 완료
  // → 배열 data 전달
  // → 배열 길이 출력
  //
  // 앞의 await는 전체 체인이 끝난 뒤 다음 예제로 넘어가게 합니다.
  await promise
    // 화살표 함수의 식 본문이므로 res.json()의 반환값을 자동 반환합니다.
    // 반환한 Promise가 완료되어야 다음 then이 실행됩니다.
    .then(res => res.json())

    // 앞선 json()의 완료 결과인 DB 배열을 전달받습니다.
    .then(data => console.log('  then으로 받은 개수:', data.length)) // 2

    // 요청 실패 또는 앞선 then 내부에서 발생한 에러를 처리합니다.
    // 단, HTTP 404 같은 상태는 직접 검사하지 않으면 여기로 오지 않습니다.
    .catch(err => console.log('  실패:', err.message));


  // ── 3. async / await: Promise를 위에서 아래로 읽히게 쓰기 ──
  //
  // async : 함수가 Promise를 반환하도록 만듭니다.
  // await : Promise의 완료를 기다린 뒤 성공 결과를 꺼냅니다.
  //
  // await 중에는 해당 async 함수의 이후 실행만 대기합니다.
  // 다른 실행 가능한 작업까지 전부 멈추는 것은 아닙니다.
  //
  // await한 Promise가 실패하면 그 위치에서 예외가 발생합니다.
  console.log('\n[3] async/await');

  // 첫 번째 await: 응답 객체를 기다립니다.
  // res에는 ok, status, json()이 있습니다.
  const res = await fakeFetch('/todos/2');

  // 두 번째 await: 응답 본문의 데이터를 기다립니다.
  //
  // 실제 fetch에서는 응답을 받은 뒤에도 본문을 읽고 JSON을 파싱하는
  // 과정이 비동기이므로 res.json()에도 await가 필요합니다.
  const todo = await res.json();

  // todo는 Promise나 응답 객체가 아니라 실제 할 일 객체입니다.
  // { id: 2, title: 'React 공부', done: true }
  console.log('  ', todo.title); // React 공부


  // ── 4. 에러 처리: try / catch / finally ─────────────────
  //
  // try     : 실패할 수 있는 작업 실행
  // catch   : try에서 발생한 예외 처리
  // finally : 성공 또는 실패와 관계없이 마무리 작업 실행
  //
  // React 화면의 "로딩 중 → 성공 또는 에러" 흐름을 흉내 냅니다.
  console.log('\n[4] 로딩 / 성공 / 에러 상태 흉내');

  async function loadTodo(url) {
    // 요청을 시작할 때의 상태입니다.
    //
    // loading : 데이터를 가져오는 중인지 여부
    // data    : 성공했을 때 받은 데이터
    // error   : 실패했을 때 표시할 에러 메시지
    //
    // const는 state 변수의 재할당을 막습니다.
    // state.loading 같은 객체 속성값은 변경할 수 있습니다.
    //
    // 참고: 일반 객체이므로 값을 변경해도 React 화면이 자동으로
    // 갱신되지는 않습니다. 실제 React에서는 상태 관리가 필요합니다.
    const state = { loading: true, data: null, error: null };

    try {
      // 네트워크 실패(/down)라면 이 await에서 예외가 발생하고
      // 아래 코드를 건너뛴 뒤 catch로 이동합니다.
      const res = await fakeFetch(url);

      // [중요] 실제 fetch는 HTTP 404·500 응답만으로 실패하지 않습니다.
      // HTTP 응답을 받았다면 Promise는 정상적으로 완료될 수 있습니다.
      //
      // 따라서 res.ok를 확인하여 실패 상태를 직접 예외로 바꿉니다.
      //
      // !res.ok는 "ok가 false이면"이라는 뜻입니다.
      // throw 이후에는 try의 나머지 코드를 건너뛰고 catch로 이동합니다.
      if (!res.ok) throw new Error(`요청 실패 (${res.status})`);

      // 성공한 경우 응답 본문을 읽고 data에 저장합니다.
      // 실제 res.json()은 본문이 올바른 JSON이 아니면 실패할 수 있으며,
      // 그때도 아래 catch가 처리합니다.
      state.data = await res.json();
    } catch (error) {
      // 이 예제에서 받는 주요 에러:
      // 1. 네트워크 실패: "Failed to fetch"
      // 2. HTTP 실패를 직접 변환한 에러: "요청 실패 (404)"
      //
      // Error 객체의 message 속성에 설명 문자열이 들어 있습니다.
      state.error = error.message;
    } finally {
      // 성공하든 실패하든 요청 처리가 끝났으므로 로딩을 종료합니다.
      // 실제 화면에서는 로딩 표시를 숨기는 처리에 해당합니다.
      state.loading = false;
    }

    // async 함수이므로 state 자체가 즉시 반환되는 것이 아니라
    // state를 성공 결과로 갖는 Promise가 반환됩니다.
    //
    // 여기서는 에러를 catch에서 처리하고 다시 throw하지 않았으므로
    // 요청에 실패해도 loadTodo의 Promise는 state로 정상 완료됩니다.
    return state;
  }

  // await로 최종 상태 객체를 받은 뒤 JSON.stringify로 문자열로 바꿉니다.
  // 세 호출 모두 await하므로 한 요청이 끝난 다음 요청을 시작합니다.

  // 성공: data에 할 일이 들어가고 error는 null
  console.log('  ', JSON.stringify(await loadTodo('/todos/1')));
  // {"loading":false,"data":{"id":1,"title":"장보기","done":false},"error":null}

  // HTTP 실패: 응답은 왔지만 해당 데이터가 없음
  console.log('  ', JSON.stringify(await loadTodo('/todos/99')));
  // {"loading":false,"data":null,"error":"요청 실패 (404)"}

  // 네트워크 실패: 응답을 받지 못함
  console.log('  ', JSON.stringify(await loadTodo('/down')));
  // {"loading":false,"data":null,"error":"Failed to fetch"}


  // ── 5. 여러 요청을 동시에: Promise.all ──────────────────
  console.log('\n[5] 순서대로 vs 동시에');

  // Date.now()는 현재 시각을 밀리초 단위의 숫자로 반환합니다.
  // 종료 시각 - 시작 시각으로 경과 시간을 구할 수 있습니다.
  let start = Date.now();

  // [순차 실행]
  // 첫 번째 요청이 끝난 후 두 번째 요청을 시작합니다.
  //
  // 첫 번째 요청 약 100ms + 두 번째 요청 약 100ms
  // → 전체 약 200ms
  await fakeFetch('/todos/1');
  await fakeFetch('/todos/2');

  // / 100 → 반올림 → * 100으로 100ms 단위의 근삿값을 출력합니다.
  // 실행 환경에 따라 실제 측정값은 달라질 수 있습니다.
  console.log(`  순서대로 두 번: 약 ${Math.round((Date.now() - start) / 100) * 100}ms`);


  // [동시 진행]
  start = Date.now();

  // 배열을 만들면서 fakeFetch 두 개를 연속 호출합니다.
  // 첫 번째 요청의 완료를 기다리지 않고 두 번째 요청도 시작합니다.
  //
  // Promise.all은 전달받은 Promise가 모두 성공하기를 기다립니다.
  // 대기 시간이 겹치므로 전체 시간은 약 100ms입니다.
  //
  // 중요:
  // - 결과 배열의 순서는 완료 순서가 아니라 입력 배열 순서입니다.
  // - 하나라도 rejected가 되면 Promise.all도 rejected가 됩니다.
  // - 다른 요청이 자동으로 취소되지는 않습니다.
  // - HTTP 404는 fakeFetch 자체를 rejected로 만들지 않습니다.
  //
  // 현재 results에는 본문 데이터가 아니라 응답 객체 2개가 들어갑니다.
  // 본문을 얻으려면 각 응답의 json()을 호출해야 합니다.
  const results = await Promise.all([
    fakeFetch('/todos/1'),
    fakeFetch('/todos/2'),
  ]);

  console.log(`  Promise.all:    약 ${Math.round((Date.now() - start) / 100) * 100}ms, 결과 ${results.length}개`);

  // 참고: 응답 본문까지 모두 읽으려면 다음처럼 작성할 수 있습니다.
  //
  // const todos = await Promise.all(results.map(res => res.json()));
  // console.log(todos);
  //
  // 서로 독립적인 요청은 동시에 진행할 수 있지만,
  // 앞선 요청의 결과가 필요한 요청은 순서대로 실행해야 합니다.
  // 예: 로그인 결과로 받은 토큰을 이용하여 내 정보 요청


  // ── 6. 에러 직접 만들기 ─────────────────────────────────
  //
  // 기본 Error에는 message, name 등의 정보가 있습니다.
  // 여기에 HTTP 상태 코드 등 추가 정보를 담으려면 확장할 수 있습니다.
  //
  // extends Error: Error 클래스를 상속하여 사용자 정의 에러 생성
  class ApiError extends Error {
    // new ApiError(404, '없는 할 일입니다.')로 생성하면 호출됩니다.
    constructor(status, message) {
      // 부모 Error 생성자를 호출하여 message를 설정합니다.
      // 상속받은 클래스에서는 this 사용 전에 super()를 호출해야 합니다.
      super(message);

      // 기본 Error에는 없는 status 속성을 추가합니다.
      this.status = status;
    }
  }

  console.log('\n[6] 에러 클래스');

  try {
    // new는 에러 객체를 만들고, throw는 그 객체를 예외로 던집니다.
    // 여기서 정상 실행 흐름이 중단되고 아래 catch로 이동합니다.
    throw new ApiError(404, '없는 할 일입니다.');
  } catch (error) {
    // 직접 추가한 status와 부모 Error가 제공한 message를 사용합니다.
    console.log(`  ${error.status}: ${error.message}`); // 404: 없는 할 일입니다.

    // instanceof로 어떤 클래스의 객체인지 확인할 수 있습니다.
    // 에러 종류에 따라 서로 다르게 처리할 때 유용합니다.
    console.log('  ApiError인가?', error instanceof ApiError); // true

    // ApiError는 Error를 상속하므로 error instanceof Error도 true입니다.
  }


  // ── 7. 자주 하는 실수: await를 빠뜨림 ──────────────────
  console.log('\n[7] await 를 빠뜨리면');

  // await 없이 호출했으므로 forgot에는 Promise가 들어갑니다.
  // 요청 자체는 이미 시작되지만 아직 응답 객체를 꺼내지 않았습니다.
  const forgot = fakeFetch('/todos');

  // ok는 응답 객체의 속성입니다.
  // Promise에는 ok 속성이 없으므로 undefined가 나옵니다.
  //
  // Promise가 나중에 완료되어도 forgot 변수 자체가
  // 응답 객체로 바뀌는 것은 아닙니다. 계속 Promise를 참조합니다.
  console.log('  forgot.ok =', forgot.ok); // undefined

  // 시작한 작업이 끝날 때까지 기다립니다.
  // 이 줄에서는 완료 결과를 별도 변수에 저장하지 않습니다.
  await forgot;

  // 올바르게 응답의 ok를 확인하는 방법:
  //
  // const response = await fakeFetch('/todos');
  // console.log(response.ok); // true
}


// main 함수를 호출하여 예제를 실행합니다.
// main()도 Promise를 반환하지만 여기서는 반환값을 사용하지 않습니다.
//
// 실제 프로그램에서 처리되지 않은 실패까지 받으려면
// main().catch(error => console.error('실행 실패:', error));
// 형태로 최상위 에러 처리를 추가할 수 있습니다.
main();


// ============================================================
// React에서는 이렇게 쓰입니다
// ============================================================
//
// 1. API 호출 함수
//    const res = await fetch(url);
//    if (!res.ok) throw new ApiError(res.status, '요청 실패');
//    return await res.json();
//
//    → 응답 상태 확인과 데이터 읽기를 담당합니다.
//
// 2. 폼 제출
//    try {
//      await onSubmit(values);
//      // 성공했을 때 입력창 초기화 등의 처리
//    } catch {
//      // 실패했을 때 입력값 유지 및 에러 표시
//    }
//
//    → await해야 제출이 실제로 완료된 뒤 성공 처리를 할 수 있습니다.
//
// 3. 여러 항목 삭제
//    await Promise.all(ids.map(id => deleteTodo(id)));
//
//    → map으로 각 삭제 작업을 시작하고 Promise 배열을 만듭니다.
//    → Promise.all로 모든 삭제 작업의 성공을 기다립니다.
//    → 일부 실패 시 이미 성공한 삭제가 자동으로 복구되지는 않습니다.
//
// 4. 화면 상태
//    isPending → 로딩 표시
//    isError   → 에러 안내
//    data      → 목록 표시
//
//    → 이러한 이름은 사용하는 상태 관리 도구에 따라 달라집니다.
//    → Promise 자체가 React 화면 상태를 자동으로 관리하지는 않습니다.
// ============================================================
