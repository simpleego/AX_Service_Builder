import { useCallback, useEffect, useState } from 'react'

// Todo 목록을 불러오고 추가·수정·삭제하는 Hook.
// authRequest는 useAuth에서 받는다. 토큰을 붙이고 만료 시 갱신하는 일은 그쪽이 맡는다.
export function useTodos(authRequest) {
  const [todos, setTodos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  // 모든 요청을 같은 방식으로 감싸 로딩·오류 상태를 관리한다.
  const run = useCallback(async (job) => {
    setLoading(true)
    setError('')
    try {
      await job()
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [])

  const load = useCallback(
    () =>
      run(async () => {
        const page = await authRequest('/api/todos?page=1&limit=100')
        setTodos(page.data)
      }),
    [authRequest, run],
  )

  // 화면이 처음 나타날 때 목록을 불러온다.
  useEffect(() => {
    load()
  }, [load])

  const add = (title) =>
    run(async () => {
      const todo = await authRequest('/api/todos', { method: 'POST', body: { title } })
      setTodos((prev) => [todo, ...prev])
    })

  const toggle = (todo) =>
    run(async () => {
      const updated = await authRequest(`/api/todos/${todo.id}`, {
        method: 'PATCH',
        body: { completed: !todo.completed },
      })
      setTodos((prev) => prev.map((t) => (t.id === updated.id ? updated : t)))
    })

  const remove = (id) =>
    run(async () => {
      await authRequest(`/api/todos/${id}`, { method: 'DELETE' })
      setTodos((prev) => prev.filter((t) => t.id !== id))
    })

  return { todos, loading, error, load, add, toggle, remove }
}
