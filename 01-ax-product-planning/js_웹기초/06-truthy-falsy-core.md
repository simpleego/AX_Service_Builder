# 06. Truthy/Falsy 핵심 원리

## 핵심 1줄
엔진은 true/false가 필요한 자리에 다른 값이 오면 `ToBoolean()` 변환기를 돌린다.
if(value) -> if(Boolean(value))

## 변환 규칙
1. falsy 6개? -> false
2. 아니면 -> true

- 논리적 없음: false
- 숫자적 없음: 0, NaN
- 존재 없음: "", null, undefined
- 그 외 존재함: [], {}, "0"

## 적용되는 3개 자리
1. if, while, for 조건
2. !, &&, || 
3. Boolean()

## &&, ||는 원본 값을 리턴
```js
0 || 100 // 100
"hello" || 100 // "hello"
0 && "실행" // 0
1 && "실행" // "실행"
```

## 원칙
"없음" 정의가 null/undefined면 ??, ?.
0,""까지 없음이면 ||, !
