import { useRef, useState } from 'react';

/** 입력 후 Enter → 추가. 추가가 끝나면 useRef로 입력칸에 다시 포커스. */
export default function TodoForm({ onAdd }) {
  const [title, setTitle] = useState('');
  const [saving, setSaving] = useState(false);
  const inputRef = useRef(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    setSaving(true);
    const ok = await onAdd(trimmed);
    setSaving(false);
    if (ok) setTitle('');
    inputRef.current?.focus();
  };

  return (
    <form className="todo-form" onSubmit={handleSubmit}>
      <input
        ref={inputRef}
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        placeholder="할 일을 입력하고 Enter"
        maxLength={200}
        aria-label="새 할 일"
      />
      <button className="btn primary" disabled={saving || !title.trim()}>
        추가
      </button>
    </form>
  );
}
