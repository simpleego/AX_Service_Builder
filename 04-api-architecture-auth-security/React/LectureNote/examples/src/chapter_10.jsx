import React, { useState } from 'react';
const initialStudents = [
  { id: 1, name: 'Inje', present: false },
  { id: 2, name: 'Steve', present: false },
  { id: 3, name: 'Bill', present: false },
];
export default function AttendancePractice() {
  const [students, setStudents] = useState(initialStudents);
  const [query, setQuery] = useState('');
  function toggle(id) {
    setStudents(previous => previous.map(student => student.id === id
      ? { ...student, present: !student.present } : student));
  }
  const visible = students.filter(student => student.name.toLowerCase().includes(query.toLowerCase()));
  return <section><label>학생 검색 <input value={query} onChange={event => setQuery(event.target.value)} /></label>
    <p>출석: {students.filter(student => student.present).length} / {students.length}</p>
    <button onClick={() => setStudents(previous => [...previous].reverse())}>순서 뒤집기</button>
    {visible.length === 0 ? <p>검색 결과가 없습니다.</p> : <ul>{visible.map(student =>
      <li key={student.id}><label><input type="checkbox" checked={student.present} onChange={() => toggle(student.id)} />{student.name}</label></li>
    )}</ul>}
  </section>;
}
