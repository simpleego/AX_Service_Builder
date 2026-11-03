# Todo 프론트엔드 (v01-rest) 설명서

v01 백엔드(FastAPI REST API)와 함께 동작하는 **React + Vite** 기반 할 일(Todo) 화면입니다.
v01 단계에는 로그인이 없으며, 서버가 모든 요청을 **공용 실습 계정(1번)** 으로 처리합니다.

---

## 1. 빠르게 실행하기

### 준비물
- **Node.js** 18 이상 (확인: `node -v`)
- **v01 백엔드**가 실행 중이어야 합니다 (MySQL DB 연결 포함)

### 실행 순서

**① 백엔드 실행** — `v01-rest` 폴더에서

```bash
# 가상환경 활성화 (Windows)
.venv\Scripts\activate

uvicorn app.main:app --reload --port 8000
```

브라우저에서 http://localhost:8000/health 에 접속했을 때 `{"status":"ok"}`가 보이면 정상입니다.

**② 프론트엔드 실행** — `v01-rest/frontend` 폴더에서 (새 터미널)

```bash
npm install     # 처음 한 번만 (패키지 설치)
npm run dev     # 개발 서버 시작
```

**③ 접속** — http://localhost:5173

오른쪽 위 배지가 초록색 **"API 연결됨"** 이면 백엔드와 잘 연결된 것입니다.

### npm 명령어 정리

| 명령어 | 하는 일 |
|---|---|
| `npm install` | `package.json`에 적힌 패키지(React, Vite)를 `node_modules`에 설치 |
| `npm run dev` | 개발 서버 실행. 코드를 저장하면 화면이 자동으로 바뀜 |
| `npm run build` | 배포용 파일을 `dist/` 폴더에 생성 |
| `npm run preview` | `build`로 만든 결과물을 미리 보기 |

---

## 2. 화면 사용법

```
┌──────────────────────────────────────────────┐
│ Todo                            [API 연결됨]   │
│ v01 · REST API · 로그인 없이 공용 실습 계정…     │
│                                              │
│ [ 할 일을 입력하세요              ] [추가]       │
│                                              │
│ (전체) (진행 중) (완료)                         │
│                                              │
│ ☐ Python 공부                    [수정][삭제]   │
│   #2 · 26. 11. 2. 오후 3:34                   │
│ ☑ React 복습 (완료: 취소선 표시)   [수정][삭제]   │
│   #1 · 26. 11. 2. 오후 3:20                   │
│                                              │
│          [이전]  1 페이지  [다음]                │
└──────────────────────────────────────────────┘
```

| 하고 싶은 일 | 방법 |
|---|---|
| 할 일 추가 | 입력칸에 쓰고 **Enter** 또는 **[추가]** (1~200자) |
| 완료 표시 | 왼쪽 **체크박스** 클릭 (다시 누르면 해제) |
| 제목 수정 | 제목 **더블클릭** 또는 **[수정]** → 고친 뒤 **Enter** 저장 / **Esc** 취소 / 바깥 클릭 시 저장 |
| 삭제 | **[삭제]** → 확인 창에서 확인 |
| 골라 보기 | **전체 / 진행 중 / 완료** 필터 버튼 |
| 페이지 이동 | 아래 **[이전] / [다음]** (한 페이지에 10개) |

> 목록은 **최신순**(번호가 큰 것부터)으로 보입니다. 새로 추가하면 자동으로 1페이지로 이동합니다.

---

## 3. 폴더 구조

```
frontend/
├── index.html              # 브라우저가 처음 여는 HTML. <div id="root">에 React가 그림
├── package.json            # 프로젝트 정보와 사용하는 패키지 목록
├── vite.config.js          # 개발 서버 설정 (포트 5173, 백엔드 프록시)
├── .gitignore              # Git에 올리지 않을 파일 (node_modules, dist)
└── src/
    ├── main.jsx            # 앱 시작점: <App />을 화면에 그림
    ├── App.jsx             # 최상위 화면: 상태 관리 + 추가/수정/삭제 처리
    ├── index.css           # 전체 디자인
    ├── errors.js           # 서버 오류 코드 → 한국어 문장 변환
    ├── api/
    │   └── todos.js        # 백엔드와 통신하는 함수 모음
    └── components/
        ├── TodoForm.jsx    # 입력칸 + 추가 버튼
        └── TodoItem.jsx    # 할 일 한 줄 (체크, 제목, 수정, 삭제)
```

### 컴포넌트 관계

```
main.jsx
  └── App.jsx  ← 데이터(todos)와 처리 함수를 가지고 있음
        ├── TodoForm   (onCreate 함수를 받음)
        └── TodoItem × N   (todo 데이터, onUpdate·onDelete 함수를 받음)
```

**핵심 원칙:** 데이터는 부모(App)가 가지고, 자식은 받은 함수를 호출해 "이렇게 바꿔 줘"라고 부탁만 합니다.
자식이 직접 서버에 요청하지 않으므로 데이터 흐름을 따라가기 쉽습니다.

---

## 4. 파일별 설명

### 4-1. `api/todos.js` — 백엔드 통신

화면 코드가 주소나 요청 방식을 몰라도 되도록 통신 코드를 한곳에 모았습니다.

| 함수 | HTTP 요청 | 설명 |
|---|---|---|
| `listTodos({ page, limit, completed })` | `GET /api/todos?page=1&limit=10&completed=true` | 목록 조회 |
| `getTodo(id)` | `GET /api/todos/{id}` | 하나 조회 |
| `createTodo(title)` | `POST /api/todos` | 추가 → 201 |
| `updateTodo(id, patch)` | `PATCH /api/todos/{id}` | 바꿀 필드만 보냄 |
| `deleteTodo(id)` | `DELETE /api/todos/{id}` | 삭제 → 204 |
| `checkHealth()` | `GET /health` | 서버 상태 확인 |

모든 함수는 공통 함수 `request()`를 거칩니다.

```js
const res = await fetch(path, { ... })          // ① 서버에 요청
if (res.status === 204) return null             // ② 삭제 성공 등 내용 없는 응답
const body = await res.json()                   // ③ JSON → 자바스크립트 객체
if (!res.ok) throw new ApiError(...)            // ④ 실패면 오류를 던짐
return body                                     // ⑤ 성공이면 데이터 반환
```

**PATCH 사용 예시** — 바꾸고 싶은 항목만 보냅니다.

```js
updateTodo(3, { completed: true })   // 완료 체크만
updateTodo(3, { title: '새 제목' })   // 제목만
```

### 4-2. `App.jsx` — 최상위 화면

**상태(state)** — 값이 바뀌면 React가 화면을 자동으로 다시 그립니다.

| 상태 | 의미 |
|---|---|
| `todos` | 현재 페이지의 할 일 목록 |
| `page` | 현재 페이지 번호 |
| `filter` | `'all'` / `'active'` / `'done'` |
| `loading` | 목록을 불러오는 중인지 |
| `error` | 화면에 보여줄 오류 문장 |
| `health` | 서버 연결 상태 `'checking'` / `'ok'` / `'down'` |

**동작 흐름**

```
화면 열림 ──► useEffect ──► load() ──► listTodos() ──► setTodos() ──► 화면 갱신
                 ▲
     page·filter가 바뀌면 다시 실행

[추가/수정/삭제] ──► run(action) ──► 서버 요청 ──► 성공 시 목록 다시 불러오기
                                            └► 실패 시 오류 상자 표시
```

- 변경 후 **목록을 서버에서 다시 불러오는** 방식이라 화면이 항상 서버 데이터와 같습니다.
- 페이지의 마지막 항목을 지우면 자동으로 이전 페이지로 이동합니다.
- 백엔드가 전체 개수를 주지 않으므로, **현재 페이지가 꽉 찼을 때(10개)만** [다음] 버튼이 켜집니다.

### 4-3. `components/TodoForm.jsx` — 입력 폼

- **제어 컴포넌트:** 입력칸의 글자(`value`)와 상태(`title`)를 항상 같게 유지합니다.
- `e.preventDefault()`로 폼 제출 시 페이지가 새로고침되는 것을 막습니다.
- 서버에 보내는 동안(`busy`) 버튼을 비활성화해 중복 추가를 막습니다.
- 추가에 **성공했을 때만** 입력칸을 비웁니다 (실패하면 다시 시도할 수 있게 남겨 둠).

### 4-4. `components/TodoItem.jsx` — 할 일 한 줄

- `editing` 상태에 따라 **제목 글자** 또는 **수정 입력칸**을 보여줍니다 (조건부 렌더링).
- 제목이 실제로 바뀌었을 때만 서버에 요청합니다.
- 서버 시각은 UTC이므로 끝에 `Z`를 붙여 한국 시간으로 표시합니다.

### 4-5. `errors.js` — 오류 메시지

| 서버 오류 코드 | HTTP | 화면 문장 |
|---|---|---|
| `TODO_NOT_FOUND` | 404 | 할 일을 찾을 수 없습니다… |
| `VALIDATION_ERROR` | 422 | 입력값을 확인하세요. 제목은 1~200자… |
| `INTERNAL_ERROR` | 500 | 서버 오류가 발생했습니다… |
| (서버 꺼짐) | — | 서버에 연결할 수 없습니다… |

### 4-6. `vite.config.js` — 프록시 설정

프론트(5173)와 백엔드(8000)는 포트가 달라 브라우저가 **다른 사이트**로 봅니다.
브라우저 보안 규칙(**CORS**) 때문에 이런 요청은 막히는데, v01 백엔드에는 이를 허용하는 설정이 없습니다.

그래서 Vite 개발 서버가 요청을 **대신 전달**합니다.

```
브라우저 ──► localhost:5173/api/todos ──(Vite 프록시)──► localhost:8000/api/todos
```

백엔드 주소가 다르면 환경변수로 바꿀 수 있습니다.

```powershell
# PowerShell
$env:VITE_API_TARGET = "http://localhost:9000"; npm run dev
```

> ⚠️ 프록시는 **개발 서버(`npm run dev`)에서만** 동작합니다. `npm run build` 결과물을 실제로 배포할 때는
> 같은 도메인에서 백엔드를 서비스하거나 백엔드에 CORS 설정을 추가해야 합니다.

---

## 5. 코드에 나오는 React · JS 문법 정리

| 문법 | 뜻 | 예시 |
|---|---|---|
| `useState(초기값)` | 기억할 값(상태)과 바꾸는 함수를 만듦 | `const [page, setPage] = useState(1)` |
| `useEffect(fn, [deps])` | 화면을 그린 뒤 실행. deps가 바뀔 때마다 재실행, `[]`이면 처음 한 번 | `useEffect(() => { load() }, [load])` |
| `useCallback(fn, [deps])` | deps가 바뀔 때만 함수를 새로 만듦 | `useCallback(async () => {...}, [page, filter])` |
| props | 부모가 자식에게 넘기는 값 | `<TodoItem todo={todo} />` |
| JSX `{ }` | JSX 안에 자바스크립트 값 넣기 | `<span>{todo.title}</span>` |
| `조건 ? A : B` | 조건에 따라 A 또는 B | `busy ? '추가 중…' : '추가'` |
| `조건 && A` | 조건이 참일 때만 A 표시 | `error && <div>{error}</div>` |
| `배열.map()` | 배열로 여러 요소 만들기 (`key` 필수) | `todos.map(t => <TodoItem key={t.id} />)` |
| `async / await` | 서버 응답을 기다림 | `const res = await fetch(...)` |
| `try / catch / finally` | 시도 / 오류 처리 / 항상 실행 | `try { await load() } catch (e) { … } finally { setLoading(false) }` |
| `?.` | 값이 없어도 오류 없이 `undefined` | `body?.error` |
| `??` | 왼쪽이 없으면 오른쪽 사용 | `err.code ?? 'HTTP_500'` |
| `...객체` | 객체 펼치기(복사) | `{ ...options, headers }` |

---

## 6. 문제 해결

| 증상 | 원인 / 해결 |
|---|---|
| 배지가 빨간색 **"API 연결 안 됨"** | 백엔드가 꺼져 있음 → 8000번 포트로 백엔드 실행. DB(MySQL) 실행 여부도 확인 |
| 5173에 **다른 화면**이 보임 | 다른 프로젝트가 5173을 사용 중 → 그 서버를 끄거나, 터미널에 표시된 다른 포트(5174 등)로 접속 |
| `npm run dev` 시 `vite` 명령을 찾을 수 없음 | `npm install`을 먼저 실행 |
| "입력값을 확인하세요" 오류 | 제목이 비어 있거나 200자 초과 |
| 날짜가 9시간 어긋남 | 서버가 UTC로 저장하는지 확인 (`database.py`에서 `time_zone = '+00:00'` 설정) |
| API를 직접 확인하고 싶음 | http://localhost:8000/api/docs (Swagger 문서) |

---

## 7. 다음 단계에서 바뀔 부분

이 프론트엔드는 **v01(로그인 없음)** 기준입니다. 이후 버전에서는 다음이 추가될 예정입니다.

- 회원가입 / 로그인 화면 (JWT 인증, v03~)
- 요청마다 `Authorization` 헤더에 토큰 첨부 → `api/todos.js`의 `request()`만 수정하면 됨
- 토큰 만료 시 자동 재발급(Refresh Token)
- Google 소셜 로그인 (v04~)
