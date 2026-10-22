// ============================================================
// 02. 비교, 논리 연산자, 조건문
// 실행: node lessons/02-conditions.js
// ============================================================
// React 화면은 "조건에 따라 다르게 보여 주기"의 연속입니다.
// 로딩 중이면 스피너, 에러면 에러 문구, 목록이 비면 안내 문구…

// ── 1. 비교: === 를 쓴다 ────────────────────────────────────
// ===  : 값과 자료형이 모두 같아야 true (항상 이것을 쓴다)
// ==   : 자료형을 멋대로 바꿔서 비교한다 (쓰지 않는다)
console.log('[1] 비교');
console.log(1 === 1);     // true
console.log('1' === 1);   // false ← 문자열과 숫자는 다르다
console.log('1' == 1);    // true  ← == 는 이런 혼란을 만든다
console.log(3 !== 4);     // true  ← 같지 않다
console.log('2026-10-20' < '2026-10-25'); // true ← 'YYYY-MM-DD' 문자열은 크기 비교가 날짜 순서와 같다

// ── 2. if / else ────────────────────────────────────────────
const score = 85;
let grade;
if (score >= 90) {
  grade = 'A';
} else if (score >= 80) {
  grade = 'B';
} else {
  grade = 'C';
}
console.log('\n[2] if/else:', grade); // B

// ── 3. 삼항 연산자: 조건 ? 참일때값 : 거짓일때값 ────────────
// if문은 "값"이 아니라서 JSX 안에 쓸 수 없다. 그래서 React에서는 삼항 연산자를 쓴다.
const done = true;
const label = done ? '완료' : '진행 중';
console.log('\n[3] 삼항:', label); // 완료

// ── 4. truthy와 falsy ───────────────────────────────────────
// 조건 자리에 true/false가 아닌 값이 오면, 자바스크립트가 참/거짓으로 바꿔 판단한다.
// 거짓으로 취급되는 값(falsy)은 딱 이것뿐: false, 0, '', null, undefined, NaN
// 나머지는 모두 참(truthy): '0', 'false', [], {} 도 참이다!
console.log('\n[4] truthy/falsy (Boolean으로 확인)');
console.log(Boolean(''));        // false ← 빈 문자열
console.log(Boolean('hello'));   // true
console.log(Boolean(0));         // false
console.log(Boolean([]));        // true  ← 빈 배열도 참! (자주 하는 실수)
console.log(Boolean(null));      // false

const items = [];
if (items.length === 0) console.log('목록이 비었습니다'); // 빈 배열은 length로 확인한다

// ── 5. 논리 연산자 && || ! ─────────────────────────────────
const isLoggedIn = true;
const isAdmin = false;
console.log('\n[5] 논리 연산자');
console.log(isLoggedIn && isAdmin); // false ← 둘 다 참이어야 참 (AND)
console.log(isLoggedIn || isAdmin); // true  ← 하나라도 참이면 참 (OR)
console.log(!isLoggedIn);           // false ← 반대 (NOT)
console.log(!!'hello');             // true  ← !! 는 불리언으로 바꾸는 관용구

// ── 6. && 와 || 는 "값"을 돌려준다 (React 핵심!) ─────────────
// A && B : A가 참이면 B를, 거짓이면 A를 돌려준다
// A || B : A가 참이면 A를, 거짓이면 B를 돌려준다
const error = '서버 오류';
console.log('\n[6] && || 가 돌려주는 값');
console.log(error && `에러: ${error}`); // 에러: 서버 오류
console.log(null && '보이지 않음');     // null
console.log('' || '기본값');            // 기본값

// [주의] && 왼쪽에 숫자를 두면 0이 그대로 나온다
const count = 0;
console.log(count && `${count}개`);      // 0  ← React 화면에 "0"이 찍히는 버그의 원인
console.log(count > 0 && `${count}개`);  // false ← 이렇게 비교식으로 쓴다 (React는 false를 그리지 않음)

// ── 7. ?? (null 병합) ───────────────────────────────────────
// A ?? B : A가 null 또는 undefined일 때만 B. (0과 ''은 그대로 둔다)
const savedCount = 0;
console.log('\n[7] ?? 와 || 의 차이');
console.log(savedCount || 10); // 10 ← 0을 "없음"으로 착각한다
console.log(savedCount ?? 10); // 0  ← 0은 올바른 값으로 인정한다
console.log(undefined ?? '/api'); // /api

// ── 8. ?. (옵셔널 체이닝) ───────────────────────────────────
// 앞의 값이 null/undefined이면 에러 대신 undefined를 돌려준다.
const user = null;
console.log('\n[8] ?.');
// console.log(user.name); // ← 에러! Cannot read properties of null
console.log(user?.name);             // undefined
console.log(user?.name ?? '손님');   // 손님

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// v1 App.jsx:   {visible.length === 0 ? <p>없음</p> : <ul>…</ul>}   ← 삼항
// v2 TodoForm:  {errors.title && <p>{errors.title}</p>}           ← 에러가 있을 때만 보여 주기
// v2 Layout:    <span>{user?.name}님</span>                       ← user가 없어도 에러 안 남
// v2 client.ts: import.meta.env.VITE_API_URL ?? '/api'           ← 기본값
// v2 목록 화면: searchParams.get('q') ?? ''
// ============================================================
