### Part 1. 고차함수 - 함수를 다루는 함수

**정의:** 함수를 인자로 받거나, 함수를 리턴하는 함수. AX에서 데이터 100개를 AI에 넣기 전에 가공할 때 전부 이걸로 한다.

#### 1. 필수 5대장 - 이론 + 예시

```javascript
const users = [
  { id: 1, name: '철수', age: 25, dept: '생산', score: 80 },
  { id: 2, name: '영희', age: 31, dept: '생산', score: 92 },
  { id: 3, name: '민수', age: 28, dept: '품질', score: 75 },
  { id: 4, name: '지은', age: 35, dept: '품질', score: 88 },
];

// 1) map: 모양 바꾸기 (1개 -> 1개 변환)
const names = users.map(user => user.name);
// 결과: ['철수', '영희', '민수', '지은']

const forAI = users.map(u => `이름:${u.name}, 점수:${u.score}점`);
// 결과: ["이름:철수, 점수:80점", ...] -> 이걸 프롬프트에 넣음

// 2) filter: 거르기 (조건에 맞는 것만)
const highScore = users.filter(u => u.score >= 85);
// 결과: 영희, 지은만 남음

// 3) reduce: 누적/합계 (배열 -> 하나의 값)
const totalScore = users.reduce((합계, 현재사람) => 합계 + 현재사람.score, 0);
const avgScore = totalScore / users.length; // 83.75

// RAG에서 자주 쓰는 reduce - 부서별 그룹화
const byDept = users.reduce((acc, cur) => {
  if(!acc[cur.dept]) acc[cur.dept] = [];
  acc[cur.dept].push(cur.name);
  return acc;
}, {});
// 결과: { 생산: ['철수','영희'], 품질: ['민수','지은'] }

// 4) sort: 정렬 (원본을 바꿈, 주의!)
const sorted = [...users].sort((a,b) => b.score - a.score); // 점수 높은 순
// [...users]로 복사 후 sort 해야 원본이 안 망가짐

// 5) forEach: 그냥 반복 (리턴 없음, map이랑 헷갈리면 안됨)
users.forEach(u => console.log(`${u.name}님 처리 중...`));
```

#### 2. 고차함수 직접 만들기 - 이걸 이해하면 레벨업

```javascript
// 함수를 리턴하는 고차함수
function createLogger(prefix) {
  return function(message) {
    console.log(`[${prefix}] ${message}`);
  }
}

const aiLogger = createLogger('AI');
const dbLogger = createLogger('DB');

aiLogger('호출 시작'); // [AI] 호출 시작
dbLogger('연결 성공'); // [DB] 연결 성공

// AX 실무용: 권한 체크하는 고차함수
function withAuth(fn) {
  return async function(...args) {
    const token = localStorage.getItem('token');
    if(!token) throw new Error('로그인 필요');
    return await fn(...args); // 원래 함수 실행
  }
}

const secureChat = withAuth(chat); // chat 함수는 토큰 체크가 자동으로 붙음
```

---

### Part 2. 동기 vs 비동기 - 수업에서 가장 중요한 파트

```javascript
// [실습 1] 동기: 줄 서서 기다리기
console.log('1. 주문');
console.log('2. 커피 만듦 - 3초 걸림... (여기서 앱이 멈춤)');
console.log('3. 서빙');

// [실습 2] 비동기: 번호표 주기
console.log('1. 주문');

setTimeout(() => {
  console.log('2. 커피 완성! (3초 뒤에 따로 실행됨)');
}, 3000);

console.log('3. 서빙 먼저 함 (기다리지 않음)');
// 실행 순서: 1 -> 3 -> (3초 후) 2
```

#### 비동기 진화 3단계

```javascript
// 1단계: 콜백 (옛날 방식, 지금은 쓰지 마세요 - 예시용)
function getUserCallback(id, callback) {
  setTimeout(() => callback({id, name: '철수'}), 1000);
}
getUserCallback(1, (user) => {
  console.log(user);
});

// 2단계: Promise (현재 표준의 뼈대)
function getUserPromise(id) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      if(id > 0) resolve({id, name: '철수'});
      else reject('ID 오류');
    }, 1000);
  });
}

getUserPromise(1)
 .then(user => console.log('성공', user))
 .catch(err => console.log('실패', err));

// 3단계: async/await (Promise를 동기처럼 쓰기 - 지금은 무조건 이거)
async function 수업용_예제() {
  try {
    console.log('유저 조회 시작...');
    const user = await getUserPromise(1); // 1초 기다림
    console.log('조회 성공:', user);

    const posts = await getUserPromise(user.id); // user 결과로 또 호출
    console.log('게시물까지 조회:', posts);
  } catch (err) {
    console.error('에러 발생:', err);
  }
}
수업용_예제();
```

### Part 3. 수업용 통합 실습 - AI 로그 분석기 만들기

학생들에게 이 코드를 주고 3개 미션을 시켜봐. 15분이면 끝난다.

```javascript
// === 데이터 ===
const aiLogs = [
  { user: '철수', prompt: '불량 원인?', tokens: 120, success: true, time: 1.2 },
  { user: '영희', prompt: '보고서 써줘', tokens: 800, success: true, time: 3.5 },
  { user: '철수', prompt: '번역해줘', tokens: 50, success: false, time: 0.8 },
  { user: '민수', prompt: '코드 짜줘', tokens: 600, success: true, time: 2.9 },
];

// === 미션 1: 고차함수 기초 (5분) ===
console.log('--- 미션1: 성공한 요청만 뽑아서 프롬프트 목록 만들기 ---');
// 힌트: filter -> map
const successPrompts = aiLogs
 .filter(log => log.success)
 .map(log => log.prompt);
console.log(successPrompts);

// === 미션 2: reduce 활용 (5분) ===
console.log('--- 미션2: 유저별 토큰 사용량 합계 ---');
// 힌트: reduce로 { 철수: 170, 영희: 800 ... } 만들기
const tokenByUser = aiLogs.reduce((acc, log) => {
  acc[log.user] = (acc[log.user]||0) + log.tokens;
  return acc;
}, {});
console.log(tokenByUser);

// === 미션 3: 비동기 + 고차함수 (10분) - AX 핵심 ===
console.log('--- 미션3: 모든 로그를 AI로 요약하기 (가상 API) ---');

// 가짜 AI API (1초 걸리는 비동기 함수)
function fakeAISummary(prompt) {
  return new Promise(resolve => {
    setTimeout(() => resolve(`'${prompt}' 요약 완료`), 1000);
  });
}

async function runAllSummary() {
  // 동기식으로 하면 4초 걸림
  // for(const log of aiLogs) { await fakeAISummary(log.prompt); }

  // 비동기 병렬 처리 - Promise.all + map (AX 정석)
  console.time('병렬 처리');
  const promises = aiLogs.map(log => fakeAISummary(log.prompt));
  const results = await Promise.all(promises);
  console.timeEnd('병렬 처리'); // 약 1초만에 4개가 동시에 끝남
  console.log(results);
}

runAllSummary();
```

**학생들에게 던질 질문 3개:**

1.  `map` vs `forEach` 차이? -> `map`은 새 배열을 리턴해서 AI에 넘길 데이터를 만들 때, `forEach`는 그냥 로그 찍을 때
2.  `Promise.all`을 안 쓰고 `for...of + await`로 하면 왜 느릴까? -> AI 10개 호출하면 10초 vs 1초 차이
3.  `reduce`가 왜 RAG에서 필수일까? -> 문서 100개를 부서별, 날짜별로 그룹화해야 토큰을 아낄 수 있음

이 파일 그대로 `.html`로 만들어서 드릴까? 버튼 누르면 실행되는 실습 페이지로 만들어줄게.


# 04. 고차함수와 동기/비동기 - 수업용 실습

## 고차함수 5대장
```js
const names = users.map(u => u.name);
const highScore = users.filter(u => u.score >= 85);
const total = users.reduce((acc, cur) => acc + cur.score, 0);
const sorted = [...users].sort((a,b) => b.score - a.score);
users.forEach(u => console.log(u.name));
```

## 고차함수 만들기
```js
function createLogger(prefix){
  return function(message){ console.log(`[${prefix}] ${message}`); }
}
function withAuth(fn){
  return async function(...args){
    const token = localStorage.getItem('token');
    if(!token) throw new Error('로그인 필요');
    return await fn(...args);
  }
}
```

## 동기 vs 비동기
```js
console.log('1 주문');
setTimeout(()=> console.log('2 커피 완성'), 3000);
console.log('3 서빙'); // 순서 1->3->2

function getUserPromise(id){
  return new Promise((resolve, reject)=>{
    setTimeout(()=> id>0 ? resolve({id, name:'철수'}) : reject('ID 오류'), 1000);
  });
}

async function example(){
  try{
    const user = await getUserPromise(1);
  } catch(err){ console.error(err); }
}
```

## 통합 실습: AI 로그 분석기
practice/lab-higher-order-async.js 참고
