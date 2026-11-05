import { memo, useEffect, useRef, useState } from 'react';

/**
 * Todo 한 줄. 더블클릭하면 제목 수정.
 * - React.memo: props(todo, 함수들)가 그대로면 다시 그리지 않는다.
 *   useTodos의 함수들이 useCallback으로 고정되어 있어서 memo가 효과를 낸다.
 * - useState: 수정 모드 여부, 수정 중인 제목
 * - useRef + useEffect: 수정 모드로 바뀌면 입력칸에 포커스하고 전체 선택
 */
function TodoItem({ todo, onToggle, onRename, onRemove }) {
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState(todo.title);
  const inputRef = useRef(null);

  useEffect(() => {
    if (editing) inputRef.current?.select();
  }, [editing]);

  const startEdit = () => {
    setDraft(todo.title);
    setEditing(true);
  };

  const save = async () => {
    const trimmed = draft.trim();
    if (!trimmed || trimmed === todo.title) {
      setEditing(false);
      return;
    }
    if (await onRename(todo, trimmed)) setEditing(false);
  };

  const handleKeyDown = (event) => {
    if (event.key === 'Enter') save();
    if (event.key === 'Escape') setEditing(false);
  };

  return (
    <li className={`todo-item${todo.completed ? ' done' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onToggle(todo)}
        aria-label={`${todo.title} 완료 표시`}
      />
      {editing ? (
        <input
          ref={inputRef}
          className="edit"
          value={draft}
          maxLength={200}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={handleKeyDown}
          onBlur={save}
        />
      ) : (
        <span className="title" onDoubleClick={startEdit} title="더블클릭하여 수정">
          {todo.title}
        </span>
      )}
      <time className="muted small" dateTime={todo.created_at}>
        {new Date(`${todo.created_at}Z`).toLocaleDateString('ko-KR', { month: 'short', day: 'numeric' })}
      </time>
      <button className="btn ghost icon danger" onClick={() => onRemove(todo)} aria-label={`${todo.title} 삭제`}>
        ✕
      </button>
    </li>
  );
}

export default memo(TodoItem);
