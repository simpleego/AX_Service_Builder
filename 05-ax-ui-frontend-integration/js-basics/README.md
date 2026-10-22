# React를 위한 자바스크립트 기초 (비전공자용)

React 수업 전에 꼭 알아야 할 자바스크립트만 골라 11단원으로 정리했습니다.
자바스크립트 전체를 다루지 않고, **React 코드를 읽고 고치는 데 실제로 쓰이는 문법**만 다룹니다.

각 단원은 세 단계로 공부합니다.

1. **개념 예제 읽기** (`lessons/`): 실행해서 결과를 보고, 주석의 설명과 비교합니다.
2. **연습문제 풀기** (`exercises/`): 빈칸을 채우고 실행하면 자동으로 채점됩니다.
3. **정답 확인** (`solutions/`): 다 풀었거나 30분 이상 막혔을 때만 엽니다.

모든 단원 끝에는 **"React에서는 이렇게 쓰입니다"** 상자가 있습니다. 배운 문법이 React 예제(v1 `react-mini`, v2 `react-todo-v2`)의 어디에 나오는지 보여 줍니다.

---

## 0. 준비

### 설치

1. **Node.js** (20 이상): https://nodejs.org 에서 LTS 버전 설치
2. **VS Code**: https://code.visualstudio.com
3. **Chrome** 브라우저 (10단원에서 사용)

### 터미널 사용법 (처음이라면)

VS Code에서 이 폴더(`js-basics`)를 열고, 메뉴의 **터미널 → 새 터미널**을 엽니다. 아래 명령을 입력하고 Enter를 누릅니다.

```bash
node -v
```

`v20.x.x` 같은 숫자가 나오면 준비 완료입니다.

### 파일 실행하기

```bash
node lessons/01-variables.js
```

- `node 파일경로` = 그 자바스크립트 파일을 실행하라는 뜻입니다.
- 화살표 키 ↑ 를 누르면 방금 입력한 명령이 다시 나옵니다.
- 파일 이름을 몇 글자 치고 Tab 키를 누르면 자동 완성됩니다.

---

## 1. 단원 목록

| 단원 | 주제 | 이걸 모르면 React에서… |
|---|---|---|
| 01 | 변수와 자료형, 템플릿 리터럴, 문자열 | `{left}개 남음`, 주소에서 받은 id 처리를 못 한다 |
| 02 | 비교, 논리 연산자, 삼항, `??`, `?.` | 로딩·에러·빈 화면을 조건에 따라 보여 줄 수 없다 |
| 03 | 함수, 화살표 함수, 콜백 | 컴포넌트와 이벤트 처리(`onClick`)를 이해할 수 없다 |
| 04 | 객체, 구조 분해, 전개 연산자 | props를 받거나 폼 입력값을 바꿀 수 없다 |
| 05 | 배열과 map / filter / find | 목록을 화면에 그릴 수 없다 |
| 06 | 참조와 불변성 | state를 바꿨는데 화면이 안 바뀌는 버그를 고칠 수 없다 |
| 07 | 스코프와 클로저 | "버튼을 3번 눌렀는데 1만 오른다"를 이해할 수 없다 |
| 08 | 모듈 (import / export) | 파일 맨 위의 import 줄을 읽을 수 없다 |
| 09 | 비동기, Promise, async/await, 에러 처리 | 서버에서 데이터를 받아 올 수 없다 |
| 10 | DOM과 이벤트 (브라우저) | React가 무엇을 대신해 주는지 모른다 |
| 11 | 종합: 할 일 앱의 두뇌 만들기 | (모두 통과하면 React 수업 준비 완료) |

**순서대로** 공부하세요. 특히 04 → 05 → 06은 React의 핵심이라 건너뛰면 안 됩니다.

---

## 2. 단원별 공부 방법

### 개념 예제 (`lessons/`)

```bash
node lessons/05-arrays.js
```

1. 먼저 파일을 열어 주석을 읽습니다.
2. 실행해서 출력이 주석에 적힌 결과(`// 결과`)와 같은지 비교합니다.
3. **값을 바꿔서 다시 실행해 봅니다.** 숫자를 바꾸거나, 조건을 반대로 바꿔 보세요. 직접 바꿔 본 것만 기억에 남습니다.

### 연습문제 (`exercises/`)

```bash
node exercises/05-arrays.js
```

처음 실행하면 모두 ❌ 입니다. 파일을 열어 `// ▼` 와 `// ▲` 사이에 코드를 작성하고 다시 실행합니다.

```js
export function getTitles(list) {
  // ▼
  // 여기에 코드를 작성하세요     ← 이 줄을 지우고 코드를 씁니다
  // ▲
}
```

채점 결과는 이렇게 나옵니다.

```
✅ 1. 제목 목록
❌ 2. 진행 중
   기대한 값: [ 1, 3 ]
   실제 값  : undefined (아직 아무것도 돌려주지 않음)
```

- **실제 값이 `undefined`** 이면 `return`을 빠뜨린 경우가 많습니다.
- 모두 ✅ 가 되면 "🎉 모두 통과!"가 나옵니다. 다음 단원으로 넘어가세요.
- **AI에게 답을 물어보기 전에** 최소 10분은 혼자 고민하세요. 그다음 AI에게 물을 때는 "정답 코드"가 아니라 "힌트만 달라"고 요청하세요.

### 10단원 (브라우저)

`lessons/10-dom-events.html` 파일을 Chrome으로 엽니다. (파일 탐색기에서 더블클릭하거나 브라우저 창에 끌어다 놓기)
F12를 눌러 **Console** 탭을 함께 열어 두세요. 에러가 나면 여기에 빨간 글씨로 나옵니다.

연습문제 `exercises/10-dom-events.html`은 자동 채점이 없습니다. 화면에서 직접 눌러 보며 확인합니다.
코드를 고친 뒤에는 브라우저에서 **새로고침(F5)** 해야 반영됩니다.

---

## 3. 최종 점검: 이 코드를 읽을 수 있나요?

11단원까지 마쳤다면 아래 React 코드(v1 `react-mini`의 일부)를 한 줄씩 설명해 보세요.
모든 줄에 대해 "이건 몇 단원에서 배운 무엇"이라고 말할 수 있으면 React 수업을 들을 준비가 된 것입니다.

```jsx
import { useState, useEffect } from 'react';                    // 08 모듈
import TodoItem from './components/TodoItem.jsx';

export default function App() {                                   // 03 함수, 08 export
  const [todos, setTodos] = useState(() =>                        // 05 배열 구조 분해, 03 화살표 함수
    JSON.parse(localStorage.getItem('todos') ?? '[]'),            // 04 JSON, 02 ??
  );
  const [filter, setFilter] = useState('all');

  useEffect(() => {                                               // 03 콜백
    localStorage.setItem('todos', JSON.stringify(todos));
  }, [todos]);

  function toggleTodo(id) {
    setTodos(todos.map(t => (t.id === id ? { ...t, done: !t.done } : t))); // 05 map, 04 전개, 06 불변성
  }

  const visible = todos.filter(t =>                               // 05 filter
    filter === 'active' ? !t.done : filter === 'done' ? t.done : true,      // 02 삼항
  );
  const left = todos.filter(t => !t.done).length;

  return (
    <main>
      <h1>할 일 ({left}개 남음)</h1>                               {/* 01 값 넣기 */}
      {visible.length === 0 ? (                                   // 02 조건부
        <p>표시할 항목이 없습니다.</p>
      ) : (
        <ul>
          {visible.map(todo => (                                  // 05 map
            <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} />  // 03 함수를 값으로 전달
          ))}
        </ul>
      )}
    </main>
  );
}
```

---

## 4. 자주 보는 에러 메시지

| 에러 메시지 | 뜻 | 흔한 원인 |
|---|---|---|
| `Cannot read properties of undefined (reading 'title')` | undefined에서 `.title`을 읽으려 함 | `find` 결과가 없음, `return` 빠뜨림 → `?.` 사용 고려 |
| `xxx is not defined` | 그런 이름의 변수가 없음 | 오타, 다른 `{ }` 안에서 만든 변수 |
| `xxx is not a function` | 함수가 아닌 것을 `( )`로 실행함 | import 이름 오타, 함수 대신 결과값을 넘김 |
| `Assignment to constant variable` | `const` 변수에 다시 값을 넣음 | `let`으로 바꾸거나, 새 변수를 만든다 |
| `Unexpected token` | 문법이 틀림 | 괄호 `( ) { } [ ]` 짝이 안 맞음, 쉼표 빠짐 |
| `Cannot use import statement outside a module` | import를 쓸 수 없는 환경 | `package.json`에 `"type": "module"`이 필요 (이 폴더에는 이미 있음) |
| `await is only valid in async functions` | async 아닌 함수 안에서 await 사용 | 함수 앞에 `async` 붙이기 |

---

## 5. 이 자료에서 뺀 것

React를 시작하는 데 필요하지 않아서 일부러 뺐습니다. React에 익숙해진 뒤 필요할 때 배우면 됩니다.

- `var`, 호이스팅, `this`, `prototype`, `call/apply/bind`: 함수형 React 컴포넌트에서는 거의 쓰지 않습니다.
- 클래스 상속의 자세한 내용: 09단원에서 `class ApiError extends Error` 한 가지 모양만 다룹니다.
- 정규식, 제너레이터, Symbol, Map/Set, 비트 연산 등
- TypeScript: v2(`react-todo-v2`) 수업 2강에서 다룹니다.

---

## 6. 강사용

| 명령 | 하는 일 |
|---|---|
| `npm run check-lessons` | 개념 예제가 모두 에러 없이 실행되는지 확인 |
| `npm run check-solutions` | 정답 파일이 모두 통과하는지 확인 |
| `npm run check-exercises` | 문제 파일 채점 (빈 상태에서는 모두 "실패"가 정상) |
| `node lib/make-exercises.js` | 정답 파일에서 `▼ ~ ▲` 사이를 비워 문제 파일을 다시 만듦 |

- **문제를 고칠 때는 `solutions/`만 고치고** `make-exercises.js`로 `exercises/`를 다시 만드세요. 그래야 문제와 정답이 항상 일치합니다. (`exercises/`의 같은 이름 파일을 덮어씁니다)
- 학생에게는 `solutions/` 폴더를 처음부터 주지 않고, 단원이 끝날 때 공개하는 방법도 있습니다.
- 정렬 문제(05-8)는 한국어 기준(`localeCompare(…, 'ko')`)으로 고정했습니다. 빼면 컴퓨터 언어 설정에 따라 결과가 달라집니다.
