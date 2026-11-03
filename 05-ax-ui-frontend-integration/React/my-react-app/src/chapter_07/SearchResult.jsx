import { useState, useEffect, useCallback, useRef } from 'react';

function SearchResult({ query }) {
  const [items, setItems] = useState([]);
  console.log('SearchResult 렌더링, query =', query);

  // query가 바뀔 때만 새 함수가 만들어집니다
  const fetchItems = useCallback(async () => {
    console.log('fetchItems 실행 (API 요청), query =', query);
    const res = await fetch(`https://dummyjson.com/products/search?q=${encodeURIComponent(query)}`);
    const data = await res.json();
    setItems(data.products ?? []);
  }, [query]);

  // 이전 렌더링의 fetchItems와 같은 함수인지 비교해서 콘솔에 표시합니다
  const prevFetchItems = useRef(null);
  useEffect(() => {
    if (prevFetchItems.current === fetchItems) {
      console.log('→ 같은 fetchItems 재사용 (useCallback 캐시)');
    } else {
      console.log('→ 새 fetchItems 함수 생성됨');
    }
    prevFetchItems.current = fetchItems;
  });

  useEffect(() => {
    console.log('useEffect 실행 → fetchItems 호출');
    fetchItems();
  }, [fetchItems]); // fetchItems가 바뀔 때(= query가 바뀔 때)만 실행됩니다

  return (
    <div>
      <button onClick={fetchItems}>새로고침</button>
      <ul>{items.map(item => <li key={item.id}>{item.title}</li>)}</ul>
    </div>
  );
}

export default SearchResult;
