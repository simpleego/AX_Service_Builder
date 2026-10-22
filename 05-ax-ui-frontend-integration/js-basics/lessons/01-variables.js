// ============================================================
// 01. 변수와 자료형
// 실행: node lessons/01-variables.js
// ============================================================
// 변수 = 값에 붙이는 "이름표".
// React에서는 화면에 보여 줄 값(이름, 개수, 목록)을 모두 변수에 담습니다.

// ── 1. const와 let ──────────────────────────────────────────
// const: 한 번 정하면 다른 값으로 바꿀 수 없다. (기본으로 이것을 쓴다)
// let  : 나중에 다른 값으로 바꿀 수 있다. (바꿀 필요가 있을 때만)
// var  : 옛날 방식. 쓰지 않는다.

const appName = '할 일 앱';
let count = 0;
count = count + 1; // let은 바꿀 수 있다
// appName = '다른 이름'; // ← 주석을 풀면 에러: const는 바꿀 수 없다

console.log('[1] const와 let');
console.log(appName, count); // 할 일 앱 1

// ── 2. 기본 자료형 ──────────────────────────────────────────
// 문자열(string), 숫자(number), 참/거짓(boolean), 없음(null, undefined)
const title = 'React 공부'; // 문자열: 작은따옴표 또는 큰따옴표
const price = 15000;          // 숫자: 정수와 소수 구분 없음
const done = false;           // 불리언: true 또는 false
const memo = null;            // null: "값이 없음"을 일부러 표시
let dueDate;                  // undefined: 아직 값을 넣지 않음

console.log('\n[2] 자료형 확인 (typeof)');
console.log(typeof title);   // string
console.log(typeof price);   // number
console.log(typeof done);    // boolean
console.log(typeof dueDate); // undefined
console.log(typeof memo);    // object  ← 자바스크립트의 유명한 예외. null은 그냥 외워 둔다.

// ── 3. 템플릿 리터럴 (백틱 ` ) ───────────────────────────────
// 문자열 안에 ${ } 로 변수나 계산식을 넣을 수 있다. React에서 아주 자주 쓴다.
const left = 3;
const message = `${appName}: ${left}개 남음`;
const old = appName + ': ' + left + '개 남음'; // 예전 방식 (+ 로 이어 붙이기)

console.log('\n[3] 템플릿 리터럴');
console.log(message); // 할 일 앱: 3개 남음
console.log(old);     // 할 일 앱: 3개 남음
console.log(`합계: ${price * 2}원`); // 합계: 30000원 ← 계산식도 넣을 수 있다

// ── 4. 문자열 다루기 ────────────────────────────────────────
const input = '   React 공부하기   ';
console.log('\n[4] 문자열 메서드');
console.log(`[${input.trim()}]`);        // [React 공부하기]  ← 앞뒤 공백 제거
console.log(input.trim().length);         // 10 ← 글자 수 (가운데 공백도 한 글자)
console.log('react'.toUpperCase());       // REACT
console.log('React 공부'.includes('공부')); // true  ← 포함 여부 (검색 기능에 사용)
console.log('2026-10-21'.slice(0, 4));    // 2026  ← 일부 자르기
console.log(String(42), Number('42'));    // 42 42  ← 문자 ↔ 숫자 변환

// ── 5. 숫자 변환에서 자주 하는 실수 ─────────────────────────
// 입력창과 주소(URL)에서 받은 값은 항상 "문자열"이다!
console.log('\n[5] 문자열 숫자 주의');
console.log('3' + 1);          // 31  ← 문자열 + 숫자 = 문자열 이어 붙이기
console.log(Number('3') + 1);  // 4
console.log(Number('abc'));    // NaN (Not a Number: 숫자가 아님)
console.log(Number.isNaN(Number('abc'))); // true

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// v1 App.jsx:   <h1>할 일 ({left}개 남음)</h1>
// v2 TodoItem:  className={`todo-item${todo.done ? ' is-done' : ''}`}
// v2 상세 화면: const todoId = Number(id);  ← 주소의 id는 문자열이라 숫자로 바꾼다
// v2 폼 제출:   values.title.trim()          ← 앞뒤 공백 제거
// ============================================================
