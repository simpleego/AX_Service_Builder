import { useState, useMemo } from 'react';

function ProductTable({ products }) {
  const [keyword, setKeyword] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [selectedId, setSelectedId] = useState(null);

  // 행을 선택할 때(selectedId 변경)는 다시 거르지 않습니다
  const visibleProducts = useMemo(() => {
    console.log('필터링 + 정렬 실행');
    return products.filter(p => p.name.toLowerCase().includes(keyword.toLowerCase()))
      .sort((a, b) => (sortBy === 'price' ? a.price - b.price : a.name.localeCompare(b.name)));
  }, [products, keyword, sortBy]);

  return (
    <div>
      <input value={keyword} onChange={e => setKeyword(e.target.value)} placeholder="검색" />
      <select value={sortBy} onChange={e => setSortBy(e.target.value)}>
        <option value="name">이름순</option>
        <option value="price">가격순</option>
      </select>
      <ul>
        {visibleProducts.map(p => (
          <li
            key={p.id}
            onClick={() => setSelectedId(p.id)}
            style={{ fontWeight: p.id === selectedId ? 'bold' : 'normal' }}
          >
            {p.name} - {p.price.toLocaleString()}원
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProductTable;