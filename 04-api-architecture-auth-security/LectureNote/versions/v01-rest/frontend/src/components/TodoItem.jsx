// =============================================================
// TodoItem.jsx — 할 일 "한 줄"을 보여주는 컴포넌트
//   [체크박스] 제목 (번호 · 만든 시각)   [수정] [삭제]
// =============================================================

import { useState } from 'react'

// 서버가 보낸 날짜 문자열을 '26. 11. 2. 오후 3:34' 같은 한국식 표기로 바꾼다.
function formatDate(value) {
  // 서버는 UTC(세계 표준시) 시각을 '2026-11-02T06:34:07'처럼 시간대 표시 없이 보낸다.
  // 끝에 'Z'(= UTC라는 표시)를 붙여야 브라우저가 한국 시간으로 올바르게 바꿔 준다.
  const date = new Date(value.endsWith('Z') ? value : `${value}Z`)
  return date.toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' })
}

// props:
//   todo     : 보여줄 할 일 데이터 { id, title, completed, created_at, updated_at }
//   onUpdate : 수정을 부모(App)에게 부탁하는 함수 (id, 바꿀 내용)
//   onDelete : 삭제를 부모(App)에게 부탁하는 함수 (id)
export default function TodoItem({ todo, onUpdate, onDelete }) {
  const [editing, setEditing] = useState(false)    // 지금 제목을 수정하는 중인지
  const [draft, setDraft] = useState(todo.title)   // 수정 중인 제목(아직 저장 전)

  // 수정 모드 시작: 현재 제목을 입력칸에 채우고 수정 모드로 바꾼다.
  function startEdit() {
    setDraft(todo.title)
    setEditing(true)
  }

  // 수정 내용 저장
  async function save() {
    const title = draft.trim()
    setEditing(false) // 먼저 수정 모드를 끈다.
    // 비어 있지 않고, 실제로 내용이 바뀌었을 때만 서버에 요청한다.
    // (바뀐 게 없는데 요청을 보내면 낭비이기 때문)
    if (title && title !== todo.title) await onUpdate(todo.id, { title })
  }

  // 수정 입력칸에서 키보드를 눌렀을 때
  function onKey(e) {
    if (e.key === 'Enter') save()              // 엔터 → 저장
    if (e.key === 'Escape') setEditing(false)  // ESC → 저장하지 않고 취소
  }

  return (
    // 완료된 할 일이면 'done' 클래스를 붙여 CSS로 취소선을 긋는다.
    <li className={`todo-item ${todo.completed ? 'done' : ''}`}>
      {/* 체크박스를 누르면 완료 상태를 반대로(true ↔ false) 바꿔 달라고 요청한다. */}
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={() => onUpdate(todo.id, { completed: !todo.completed })}
        aria-label="완료 표시"
      />

      <div className="todo-body">
        {/* 수정 중이면 입력칸을, 아니면 제목 글자를 보여준다. (조건부 렌더링) */}
        {editing ? (
          <input
            className="edit"
            value={draft}
            maxLength={200}
            autoFocus                                   // 나타나자마자 커서를 둔다.
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={onKey}
            onBlur={save}                               // 입력칸 밖을 클릭하면 저장
          />
        ) : (
          <span className="title" onDoubleClick={startEdit} title="더블클릭해서 수정">
            {todo.title}
          </span>
        )}
        <small>#{todo.id} · {formatDate(todo.created_at)}</small>
      </div>

      {/* && 연산자: 앞의 조건이 참일 때만 뒤의 버튼을 보여준다. (수정 중엔 숨김) */}
      {!editing && <button className="ghost" onClick={startEdit}>수정</button>}
      <button className="ghost danger" onClick={() => onDelete(todo.id)}>삭제</button>
    </li>
  )
}
