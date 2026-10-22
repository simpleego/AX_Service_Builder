// ============================================================
// 08. 모듈 (import / export)
// 실행: node lessons/08-modules.js
// 함께 볼 파일: lessons/modules/todo-utils.js
// ============================================================
// 코드를 파일 여러 개로 나누고, 필요한 것만 가져다 쓰는 방법입니다.
// React 프로젝트의 모든 파일은 맨 위에 import 줄로 시작합니다.

// [1] 실행하면 todo-utils.js의 console.log가 이 파일의 어떤 출력보다 먼저 찍힌다.
//     import 는 코드의 어느 줄에 있든 파일이 실행되기 "전에" 먼저 처리되기 때문이다.
//     그래서 import 는 관례적으로 파일 맨 위에 모아 쓴다.
console.log('[1] ↑ 위 줄이 먼저 찍혔다: import가 가장 먼저 실행된다');

// 기본 내보내기(default)는 { } 없이, 이름을 마음대로 붙여 가져온다
// 이름 붙인 내보내기(named)는 { } 안에 "정확한 이름"으로 가져온다
import createTodo, { countLeft, formatTodo, PRIORITY_LABEL } from './modules/todo-utils.js';

// 이름이 겹치면 as 로 바꿔서 가져온다
import { countLeft as countActive } from './modules/todo-utils.js';

// 파일 전체를 하나의 객체로 가져오기
import * as utils from './modules/todo-utils.js';

const todos = [createTodo('장보기', 'low'), { ...createTodo('공부', 'high'), done: true }];

console.log('\n[2] 가져온 것 사용');
console.log(todos.map(formatTodo)); // [ '[ ] 장보기 (낮음)', '[x] 공부 (높음)' ]
console.log(countLeft(todos));      // 1
console.log(countActive(todos));    // 1
console.log(PRIORITY_LABEL.high);   // 높음
console.log(Object.keys(utils));    // [ 'PRIORITY_LABEL', 'countLeft', 'default', 'formatTodo' ]

// ── 경로 규칙 ───────────────────────────────────────────────
// './파일'   : 지금 파일과 같은 폴더 기준 (내가 만든 파일)
// '../파일'  : 한 단계 위 폴더
// 'react'    : 경로 없이 이름만 → node_modules에 설치된 라이브러리
//
// ── 실행 환경 차이 ──────────────────────────────────────────
// Node에서 직접 실행할 때는 확장자(.js)까지 써야 한다.
// React 프로젝트(Vite)에서는 확장자를 생략해도 도구가 찾아 준다.
// 이 폴더의 package.json에 "type": "module" 이 있어서 import를 쓸 수 있다.

// ============================================================
// React에서는 이렇게 쓰입니다
// ------------------------------------------------------------
// import { useState, useEffect } from 'react';            ← 라이브러리의 named export
// import TodoForm from './components/TodoForm.jsx';        ← 내 파일의 default export
// import type { Todo } from '../types/todo';               ← (TypeScript) 타입만 가져오기
// export default function App() { … }                      ← 컴포넌트는 보통 default
// ============================================================
