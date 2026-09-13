# 03. 제시한 코드를 이해하기 위한 기초지식

## 1단계: 실행 방식
JS는 한 번에 한 줄 실행. API는 3초 걸림 -> Promise로 비동기 처리.
await는 async 안에서만 사용.

## 2단계: 객체/배열
```js
const { content } = data.choices[0].message;
const safe = data?.choices?.[0]?.message?.content ?? '응답 없음';
const merged = {...defaultConfig, baseURL: '/api'};
```

## 3단계: 함수와 문자열
- 화살표 함수: const add = (a,b) => a+b
- 템플릿 리터럴: `너는 ${company} 전문가다`

## 4단계: 모듈 시스템
```js
export const aiApi = axios.create({});
import { aiApi } from './ai.js';
```

HTTP: GET(조회), POST(생성), headers, status 200/401/429
