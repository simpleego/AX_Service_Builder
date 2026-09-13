# 05. Truthy & Falsy 수업용 예시

## Falsy 6형제
false, 0, "", null, undefined, NaN -> if에서 false

## Truthy 함정
[], {}, "0", "false", " " -> 모두 true

## AX 버그 예시
```js
let tokenCount = 0;
if(!tokenCount) console.log("버그! 0을 실패로 착각");

let score = 0;
console.log(score || 100); // 100 버그
console.log(score ?? 100); // 0 정상

let userName = "";
console.log(userName || "익명"); // 익명
console.log(userName ?? "익명"); // "" 유지
```

실습: practice/lab-truthy-falsy.js 참고
