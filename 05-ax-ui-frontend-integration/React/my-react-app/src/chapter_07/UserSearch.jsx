import { useState, useEffect, useMemo } from 'react';

function UserSearch() {
  const [name, setName] = useState('');
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const [result, setResult] = useState([]);

  console.log('Search 컴포넌트 ...')

  // ❌ const params = { name, page };  → 렌더링마다 새 객체 → effect 매번 실행
  // ✅ name이나 page가 바뀔 때만 새 객체
  const params = useMemo(() => ({ name, page }), [name, page]);

  useEffect(() => {
    console.log('검색 요청', params);
    fetch(`https://dummyjson.com/users/search?q=${params.name}&skip=${(params.page - 1) * 10}&limit=10`)
      .then(res => res.json())
      .then(data => setResult(data.users));
  }, [params]);

  return (
    <div>
      <input value={name} onChange={e => setName(e.target.value)} placeholder="이름" />
      <button onClick={() => setPage(p => p + 1)}>다음 페이지</button>
      {/* count를 바꿔도 검색 요청은 다시 가지 않습니다 */}
      <button onClick={() => setCount(c => c + 1)}>관련 없는 버튼 {count}</button>
      <ul>{result.map(u => <li key={u.id}>{u.firstName}</li>)}</ul>
    </div>
  );
}

export default UserSearch;