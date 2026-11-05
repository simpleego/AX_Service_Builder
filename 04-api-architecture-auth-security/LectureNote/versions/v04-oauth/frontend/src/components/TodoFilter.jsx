const FILTERS = [
  { value: 'all', label: '전체', count: (s) => s.total },
  { value: 'active', label: '진행 중', count: (s) => s.active },
  { value: 'done', label: '완료', count: (s) => s.done },
];

export default function TodoFilter({ value, onChange, stats }) {
  return (
    <div className="filter" role="tablist">
      {FILTERS.map((f) => (
        <button
          key={f.value}
          role="tab"
          aria-selected={value === f.value}
          className={value === f.value ? 'active' : ''}
          onClick={() => onChange(f.value)}
        >
          {f.label} <span className="count">{f.count(stats)}</span>
        </button>
      ))}
    </div>
  );
}
