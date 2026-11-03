// =============================================================
// TodoForm.jsx — "할 일 입력칸 + 추가 버튼" 컴포넌트
//
// 컴포넌트(component): 화면의 한 조각을 만드는 함수.
// 레고 블록처럼 여러 컴포넌트를 조립해서 전체 화면을 만든다.
// =============================================================

// useState: 컴포넌트가 "기억해야 하는 값(상태)"을 만드는 React 기능.
// 상태 값이 바뀌면 React가 화면을 자동으로 다시 그린다.
import { useState } from 'react'

// 제목 최대 글자 수 (백엔드 규칙과 같게 맞춤)
const MAX = 200

// props(속성): 부모 컴포넌트(App)가 넘겨준 값.
//   onCreate: "새 할 일을 추가해 줘"라고 부모에게 부탁하는 함수.
//             성공하면 true, 실패하면 false를 돌려준다.
export default function TodoForm({ onCreate }) {
  // [상태값, 상태를 바꾸는 함수] = useState(처음 값)
  const [title, setTitle] = useState('')    // 입력칸에 적힌 글자
  const [busy, setBusy] = useState(false)   // 서버에 보내는 중인지 (중복 클릭 방지용)

  // 앞뒤 공백을 뺀 제목. 공백만 입력했다면 빈 문자열('')이 된다.
  const trimmed = title.trim()

  // 폼을 제출(엔터 또는 추가 버튼 클릭)했을 때 실행되는 함수
  async function submit(e) {
    // 폼 제출 시 브라우저는 기본적으로 페이지를 새로고침한다. 이를 막는다.
    e.preventDefault()
    // 내용이 비었거나 이미 보내는 중이면 아무것도 하지 않는다.
    if (!trimmed || busy) return

    setBusy(true) // "보내는 중" 표시 → 버튼이 비활성화된다.
    try {
      // 부모에게 추가를 부탁하고, 성공했을 때만 입력칸을 비운다.
      // (실패하면 입력한 글자를 그대로 남겨 다시 시도할 수 있게 한다.)
      if (await onCreate(trimmed)) setTitle('')
    } finally {
      // finally: 성공하든 실패하든 마지막에 항상 실행된다.
      setBusy(false)
    }
  }

  // return 안의 HTML처럼 생긴 코드를 JSX라고 한다.
  // JSX 안에서 { } 중괄호를 쓰면 자바스크립트 값을 넣을 수 있다.
  return (
    <form className="todo-form" onSubmit={submit}>
      {/*
        "제어 컴포넌트" 방식의 입력칸:
        - value={title}   : 입력칸에 보이는 글자는 항상 title 상태와 같다.
        - onChange        : 사용자가 타이핑할 때마다 title 상태를 새 글자로 바꾼다.
      */}
      <input
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="할 일을 입력하세요"
        maxLength={MAX}
        aria-label="새 할 일"
      />
      {/* 내용이 없거나 보내는 중이면 버튼을 누를 수 없게(disabled) 한다. */}
      <button type="submit" disabled={!trimmed || busy}>
        {/* 삼항 연산자: 조건 ? 참일 때 값 : 거짓일 때 값 */}
        {busy ? '추가 중…' : '추가'}
      </button>
    </form>
  )
}
