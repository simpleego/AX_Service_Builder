import { useState } from 'react'
import { useTodos } from './useTodos'

// 로그인한 사용자의 Todo 목록 화면.
export default function TodoPanel({ authRequest }) {
  const { todos, loading, error, load, add, toggle, remove } = useTodos(authRequest)
  const [title, setTitle] = useState('')

  const handleAdd = async (e) => {
    e.preventDefault()
    if (!title.trim()) return
    await add(title)
    setTitle('')
  }

  return (
    <div className="card">
      <form className="row" onSubmit={handleAdd}>
        <input
          placeholder="할 일을 입력하세요"
          value={title}
          maxLength={200}
          onChange={(e) => setTitle(e.target.value)}
        />
        <button type="submit" disabled={loading}>
          추가
        </button>
        <button type="button" className="secondary" onClick={load} disabled={loading}>
          새로고침
        </button>
      </form>

      {error && <p className="message">오류: {error}</p>}

      <ul className="todos">
        {todos.map((todo) => (
          <li key={todo.id}>
            <label className={todo.completed ? 'done' : ''}>
              <input type="checkbox" checked={todo.completed} onChange={() => toggle(todo)} />
              {todo.title}
            </label>
            <button className="danger" onClick={() => remove(todo.id)}>
              삭제
            </button>
          </li>
        ))}
      </ul>
      {!loading && todos.length === 0 && <p className="empty">할 일이 없습니다.</p>}
    </div>
  )
}
