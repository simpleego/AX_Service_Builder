// =============================================================
// api/todos.js — 백엔드(FastAPI) 서버와 통신하는 함수 모음
//
// 화면 코드(App.jsx 등)는 "어떤 주소로, 어떤 방식으로" 요청하는지 몰라도 된다.
// 이 파일의 함수만 호출하면 되도록 통신 코드를 한곳에 모아 둔 것이다.
//
// v01 백엔드는 로그인이 없다. 서버가 모든 요청을 공용 계정(1번) 것으로 처리한다.
// =============================================================

// 서버가 오류를 돌려줬을 때 쓰는 "오류 객체".
// 자바스크립트 기본 Error에 status(HTTP 상태 코드)와 code(서버 오류 코드)를 더했다.
//   예) status: 404, code: 'TODO_NOT_FOUND'
export class ApiError extends Error {
  constructor(status, code, fields) {
    super(code)          // 부모(Error)의 message에 오류 코드를 넣는다.
    this.status = status // HTTP 상태 코드 (404, 422, 500 …)
    this.code = code     // 서버가 정한 오류 이름
    this.fields = fields // 입력값 검증 오류일 때 어떤 칸이 잘못됐는지 정보
  }
}

// 모든 요청이 공통으로 거치는 함수.
//   path    : 요청할 주소 (예: '/api/todos')
//   options : 요청 방식(method), 보낼 데이터(body) 등
//
// async 함수는 "시간이 걸리는 일"을 기다릴 수 있는 함수다.
// await를 붙이면 그 작업(서버 응답)이 끝날 때까지 기다렸다가 다음 줄로 간다.
async function request(path, options = {}) {
  // fetch: 브라우저에 내장된 "서버에 요청 보내기" 함수.
  // 주소가 '/api/...'처럼 상대 경로인 이유:
  //   Vite 개발 서버(vite.config.js의 proxy)가 이 요청을 백엔드(8000번 포트)로 대신 전달해 준다.
  const res = await fetch(path, {
    ...options, // 전달받은 옵션(method, body 등)을 그대로 펼쳐 넣는다.
    // 보내는 데이터가 JSON 형식이라고 서버에 알려 준다.
    headers: { 'Content-Type': 'application/json', ...options.headers },
  })

  // 204(No Content): 성공했지만 돌려줄 내용이 없다는 뜻. (삭제 성공 시)
  if (res.status === 204) return null

  // 응답 본문을 JSON → 자바스크립트 객체로 바꾼다.
  // 본문이 JSON이 아니면 오류가 나므로 .catch로 잡아 null로 처리한다.
  const body = await res.json().catch(() => null)

  // res.ok는 상태 코드가 200~299(성공)일 때 true다.
  if (!res.ok) {
    // 백엔드의 오류 응답 형식: { error: { code: '...', fields: [...] } }
    // ?. (옵셔널 체이닝): body가 null이어도 오류 없이 undefined를 돌려준다.
    // ?? (널 병합): 왼쪽 값이 없으면(null/undefined) 오른쪽 값을 쓴다.
    const err = body?.error ?? {}
    // throw: 오류를 "던져서" 이 함수를 호출한 쪽의 catch에서 처리하게 한다.
    throw new ApiError(res.status, err.code ?? `HTTP_${res.status}`, err.fields)
  }

  // 성공이면 서버가 보낸 데이터를 돌려준다.
  return body
}

// ---------------- 아래부터 실제 API 함수들 ----------------

// [목록 조회] GET /api/todos?page=1&limit=20&completed=true
//   page      : 몇 번째 페이지인지 (1부터 시작)
//   limit     : 한 페이지에 몇 개씩 가져올지
//   completed : true면 완료된 것만, false면 진행 중인 것만, 없으면 전체
export function listTodos({ page = 1, limit = 20, completed } = {}) {
  // URLSearchParams: 객체를 '?page=1&limit=20' 같은 주소 뒷부분(쿼리스트링)으로 만들어 준다.
  const params = new URLSearchParams({ page, limit })
  // '전체' 필터일 때는 completed를 아예 보내지 않는다.
  if (completed !== undefined) params.set('completed', completed)
  return request(`/api/todos?${params}`)
}

// [상세 조회] GET /api/todos/3  →  3번 할 일 하나만 가져온다.
export const getTodo = (id) => request(`/api/todos/${id}`)

// [추가] POST /api/todos  →  새 할 일을 만든다.
// JSON.stringify: 자바스크립트 객체를 서버에 보낼 수 있는 JSON 문자열로 바꾼다.
//   { title: '공부' }  →  '{"title":"공부"}'
export const createTodo = (title) =>
  request('/api/todos', { method: 'POST', body: JSON.stringify({ title }) })

// [수정] PATCH /api/todos/3  →  바꾸고 싶은 항목만 보낸다.
//   예) 완료 체크만 바꿀 때: updateTodo(3, { completed: true })
//   예) 제목만 바꿀 때    : updateTodo(3, { title: '새 제목' })
export const updateTodo = (id, patch) =>
  request(`/api/todos/${id}`, { method: 'PATCH', body: JSON.stringify(patch) })

// [삭제] DELETE /api/todos/3  →  성공하면 204(내용 없음)를 받는다.
export const deleteTodo = (id) => request(`/api/todos/${id}`, { method: 'DELETE' })

// [서버 상태 확인] GET /health  →  서버와 DB가 살아 있으면 { status: 'ok' }
export const checkHealth = () => request('/health')
