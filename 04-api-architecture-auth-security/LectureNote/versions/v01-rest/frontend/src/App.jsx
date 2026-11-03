// =============================================================
// App.jsx — 최상위 화면 컴포넌트 (앱의 "본체")
//
// 역할:
//   1) 서버에서 할 일 목록을 불러와 보관한다. (상태 관리)
//   2) 추가·수정·삭제 요청을 처리한다.
//   3) 자식 컴포넌트(TodoForm, TodoItem)에 데이터와 함수를 넘겨준다.
// =============================================================

// useState   : 기억해야 하는 값(상태)을 만든다.
// useEffect  : 화면이 그려진 "뒤에" 실행할 일(예: 서버에서 데이터 불러오기)을 등록한다.
// useCallback: 함수를 매번 새로 만들지 않고 재사용하게 해 준다.
import { useCallback, useEffect, useState } from 'react'
import { checkHealth, createTodo, deleteTodo, listTodos, updateTodo } from './api/todos.js'
import { errorMessage } from './errors.js'
import TodoForm from './components/TodoForm.jsx'
import TodoItem from './components/TodoItem.jsx'

// 한 페이지에 보여줄 할 일 개수
const LIMIT = 10

// 필터 버튼 목록.
//   key  : 프로그램 안에서 구분하는 이름
//   label: 버튼에 보이는 글자
//   value: 서버에 보낼 completed 값 (undefined면 보내지 않음 = 전체)
const FILTERS = [
  { key: 'all', label: '전체', value: undefined },
  { key: 'active', label: '진행 중', value: false },
  { key: 'done', label: '완료', value: true },
]

export default function App() {
  // ---------------- 상태(state) ----------------
  const [todos, setTodos] = useState([])          // 현재 페이지의 할 일 목록
  const [page, setPage] = useState(1)             // 현재 페이지 번호
  const [filter, setFilter] = useState('all')     // 선택된 필터 ('all' | 'active' | 'done')
  const [loading, setLoading] = useState(false)   // 목록을 불러오는 중인지
  const [error, setError] = useState('')          // 화면에 보여줄 오류 문장 ('' = 오류 없음)
  const [health, setHealth] = useState('checking') // 서버 연결 상태 ('checking' | 'ok' | 'down')

  // ---------------- 목록 불러오기 ----------------
  // 현재 page와 filter에 맞는 목록을 서버에서 가져와 todos에 저장한다.
  // useCallback의 두 번째 인자 [page, filter]:
  //   page나 filter가 바뀔 때만 이 함수를 새로 만든다.
  const load = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      // 선택된 필터의 서버용 값(true/false/undefined)을 찾는다.
      const completed = FILTERS.find((f) => f.key === filter).value
      const res = await listTodos({ page, limit: LIMIT, completed })
      // 서버 응답 형식: { data: [...할 일들], page: 1, limit: 10 }
      setTodos(res.data)
    } catch (err) {
      setError(errorMessage(err))
    } finally {
      setLoading(false)
    }
  }, [page, filter])

  // load 함수가 새로 만들어질 때마다(= page나 filter가 바뀔 때마다) 목록을 다시 불러온다.
  // 처음 화면이 열릴 때도 한 번 실행된다.
  useEffect(() => { load() }, [load])

  // 화면이 처음 열릴 때 한 번만 서버 상태를 확인한다.
  // 빈 배열 [] = "처음 한 번만 실행"이라는 뜻.
  useEffect(() => {
    checkHealth().then(() => setHealth('ok')).catch(() => setHealth('down'))
  }, [])

  // ---------------- 추가·수정·삭제 공통 처리 ----------------
  // action  : 실제로 서버에 보낼 요청 (예: () => createTodo('공부'))
  // nextPage: 요청이 끝난 뒤 이동할 페이지 (기본값: 지금 페이지)
  //
  // 변경 후에는 목록을 서버에서 다시 불러온다.
  // → 화면이 서버의 실제 데이터(정렬·필터·페이지)와 항상 같아진다.
  // 성공하면 true, 실패하면 오류를 표시하고 false를 돌려준다.
  async function run(action, nextPage = page) {
    setError('')
    try {
      await action()
      // 페이지가 바뀌면 setPage만 해도 위의 useEffect가 목록을 다시 불러온다.
      // 페이지가 그대로면 직접 load()를 호출한다.
      if (nextPage !== page) setPage(nextPage)
      else await load()
      return true
    } catch (err) {
      setError(errorMessage(err))
      return false
    }
  }

  // 추가: 새 할 일은 목록 맨 위(최신순)에 생기므로 1페이지로 이동한다.
  const handleCreate = (title) => run(() => createTodo(title), 1)

  // 수정: 완료 체크나 제목 변경
  const handleUpdate = (id, patch) => run(() => updateTodo(id, patch))

  // 삭제
  const handleDelete = (id) => {
    // confirm: 브라우저 확인 창. '취소'를 누르면 false가 되어 여기서 멈춘다.
    if (!confirm('이 할 일을 삭제할까요?')) return
    // 현재 페이지의 마지막 하나를 지우면 페이지가 텅 비므로 이전 페이지로 이동한다.
    const nextPage = todos.length === 1 && page > 1 ? page - 1 : page
    run(() => deleteTodo(id), nextPage)
  }

  // 백엔드가 "전체 개수"를 알려주지 않는다.
  // 그래서 현재 페이지가 꽉 찼으면(10개) 다음 페이지가 "있을 수도 있다"고 보고 버튼을 켠다.
  const hasNext = todos.length === LIMIT

  // ---------------- 화면 그리기 ----------------
  return (
    <main className="app">
      <header>
        <h1>Todo</h1>
        {/* 서버 상태에 따라 초록(ok)/빨강(down) 배지를 보여준다. */}
        <span className={`health ${health}`}>
          {health === 'ok' ? 'API 연결됨' : health === 'down' ? 'API 연결 안 됨' : '확인 중…'}
        </span>
      </header>
      <p className="note">v01 · REST API · 로그인 없이 공용 실습 계정을 사용합니다.</p>

      {/* 입력 폼. 추가 버튼을 누르면 handleCreate가 호출된다. */}
      <TodoForm onCreate={handleCreate} />

      {/* 필터 버튼들. 배열의 map으로 버튼 3개를 만든다. */}
      <nav className="filters">
        {FILTERS.map((f) => (
          // key: React가 목록의 각 항목을 구분하기 위한 고유 이름 (목록을 그릴 때 꼭 필요)
          <button
            key={f.key}
            className={filter === f.key ? 'active' : ''}
            // 필터를 바꾸면 1페이지부터 다시 본다.
            onClick={() => { setFilter(f.key); setPage(1) }}
          >
            {f.label}
          </button>
        ))}
      </nav>

      {/* 오류 문장이 있을 때만 빨간 상자를 보여준다. */}
      {error && <div className="error" role="alert">{error}</div>}

      {/* 상황에 따라 세 가지 중 하나를 보여준다: 불러오는 중 / 비어 있음 / 목록 */}
      {loading && todos.length === 0 ? (
        <p className="empty">불러오는 중…</p>
      ) : todos.length === 0 ? (
        <p className="empty">할 일이 없습니다.</p>
      ) : (
        <ul className="todo-list">
          {/* 할 일마다 TodoItem 컴포넌트를 하나씩 그리고, 필요한 데이터와 함수를 넘긴다. */}
          {todos.map((todo) => (
            <TodoItem key={todo.id} todo={todo} onUpdate={handleUpdate} onDelete={handleDelete} />
          ))}
        </ul>
      )}

      {/* 페이지 이동 버튼 */}
      <footer className="pager">
        <button onClick={() => setPage(page - 1)} disabled={page === 1 || loading}>이전</button>
        <span>{page} 페이지</span>
        <button onClick={() => setPage(page + 1)} disabled={!hasNext || loading}>다음</button>
      </footer>
    </main>
  )
}
