import { useTodos } from '../hooks/useTodos';
import TodoForm from '../components/TodoForm';
import TodoFilter from '../components/TodoFilter';
import TodoItem from '../components/TodoItem';
import SessionPanel from '../components/SessionPanel';

export default function TodosPage() {
  const { status, error, visibleItems, stats, filter, setFilter, reload, addTodo, toggleTodo, renameTodo, removeTodo } =
    useTodos();

  return (
    <div className="layout">
      <section className="card todos">
        <div className="todos-head">
          <h1>내 할 일</h1>
          <span className="muted">
            {stats.done}/{stats.total} 완료
          </span>
        </div>
        <TodoForm onAdd={addTodo} />
        <TodoFilter value={filter} onChange={setFilter} stats={stats} />

        {status === 'loading' && <div className="spinner small" aria-label="불러오는 중" />}
        {status === 'error' && (
          <div className="empty">
            <p className="form-error">{error}</p>
            <button className="btn" onClick={() => reload()}>
              다시 시도
            </button>
          </div>
        )}
        {status === 'ready' && visibleItems.length === 0 && (
          <p className="empty muted">{stats.total === 0 ? '첫 할 일을 추가해 보세요.' : '해당하는 할 일이 없습니다.'}</p>
        )}
        {status === 'ready' && (
          <ul className="todo-list">
            {visibleItems.map((todo) => (
              <TodoItem key={todo.id} todo={todo} onToggle={toggleTodo} onRename={renameTodo} onRemove={removeTodo} />
            ))}
          </ul>
        )}
      </section>
      <SessionPanel />
    </div>
  );
}
