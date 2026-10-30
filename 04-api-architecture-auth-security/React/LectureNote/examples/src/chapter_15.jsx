import React, { useState } from 'react';
import styled from 'styled-components';
const Wrapper = styled.div`
  display: flex;
  flex-wrap: wrap;
  align-items: flex-start;
  gap: 1rem;
  padding: 1rem;
  background: #eee;
`;
const Block = styled.div`
  padding: ${props => props.$padding};
  background: ${props => props.$backgroundColor};
  border: 1px solid #222;
  border-radius: 1rem;
  color: white;
  font-size: 2rem;
  font-weight: bold;
  text-align: center;
`;
const items = [
  { id: 'a', label: '1', padding: '1rem', color: '#b91c1c' },
  { id: 'b', label: '2', padding: '3rem', color: '#166534' },
  { id: 'c', label: '3', padding: '2rem', color: '#1e40af' },
];
export default function StylePractice() {
  const [compact, setCompact] = useState(false);
  return <section><button aria-pressed={compact} onClick={() => setCompact(previous => !previous)}>여백 모드 변경</button>
    <Wrapper>{items.map(item => <Block key={item.id} $padding={compact ? '1rem' : item.padding} $backgroundColor={item.color}>{item.label}</Block>)}</Wrapper>
  </section>;
}
