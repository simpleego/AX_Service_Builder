# JavaScript VS TypeScript
> 간단히 말하면 **JavaScript는 실행되는 언어**, **TypeScript는 JavaScript에 타입 기능을 추가한 언어**입니다.

| 구분 | JavaScript | TypeScript |
|---|---|---|
| 타입 | 동적 타입 | 정적 타입 지원 |
| 실행 | 브라우저/Node.js에서 바로 실행 | JavaScript로 변환 후 실행 |
| 오류 발견 | 주로 실행 중 발견 | 코딩/컴파일 단계에서 발견 가능 |
| 문법 | 비교적 간단 | 타입 문법이 추가됨 |
| 규모 | 소규모~대규모 | 특히 대규모 프로젝트에 유리 |
| 확장자 | `.js` | `.ts`, `.tsx` |

예를 들어 JavaScript는 다음 코드가 작성됩니다.

```javascript
function add(a, b) {
    return a + b;
}

add(10, "20");   // 결과: "1020"
```

JavaScript는 `10 + "20"`을 허용하기 때문에 예상치 못한 결과가 나올 수 있습니다.

TypeScript에서는 타입을 지정할 수 있습니다.

```typescript
function add(a: number, b: number): number {
    return a + b;
}

add(10, 20);     // 정상
add(10, "20");   // 오류
```

따라서 TypeScript의 핵심은 다음 한 문장으로 정리할 수 있습니다.

> **TypeScript = JavaScript + 타입 검사**

특히 React 기준으로 보면 요즘은 대규모 실무 프로젝트에서

```text
JavaScript
   ↓
TypeScript
   ↓
React + TypeScript
```

형태가 많이 사용됩니다.

비전공자 교육에서는 **JavaScript 기본 문법을 먼저 익힌 뒤 TypeScript를 배우는 순서**가 이해하기 좋습니다. TypeScript도 결국 실행할 때는 JavaScript로 변환되기 때문입니다.
