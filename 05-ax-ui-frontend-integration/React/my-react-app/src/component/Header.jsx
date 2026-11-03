import React from 'react';

function Header({ title }) {
  return (
    <header className="site-header">
      <p className="eyebrow">MY FIRST REACT BLOG</p>
      <h1>{title}</h1>
      <p>컴포넌트를 조합해서 만드는 나만의 블로그</p>
    </header>
  );
}

export default Header;
