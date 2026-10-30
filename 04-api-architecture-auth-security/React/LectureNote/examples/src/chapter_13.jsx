import React, { useState } from 'react';
function Card({ title, backgroundColor = 'white', children, footer }) {
  return <section className="card" style={{ backgroundColor }}>
    {title && <h3>{title}</h3>}<div>{children}</div>{footer && <footer>{footer}</footer>}
  </section>;
}
export default function CompositionPractice() {
  const [saved, setSaved] = useState(false);
  return <Card title="React 학습 카드" backgroundColor="#edf7ed"
    footer={<button onClick={() => setSaved(value => !value)}>{saved ? '저장 취소' : '저장'}</button>}>
    <p>레이아웃은 Card가, 본문과 행동은 사용하는 쪽이 결정합니다.</p>
    <p role="status">{saved ? '저장된 카드' : '저장되지 않은 카드'}</p>
  </Card>;
}
