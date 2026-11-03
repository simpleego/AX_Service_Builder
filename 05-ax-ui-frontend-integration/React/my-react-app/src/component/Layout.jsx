import React from 'react';

function Layout({ width, height, header, footer, children }) {
  return (
    // React의 숫자형 width, height 스타일 값은 px 단위로 적용됩니다.
    <div className="layout" style={{ width, height }}>
      {header}
      <main className="layout-content">
        {children ?? (
          <article>
            <p>REACT COMPONENT COMPOSITION</p>
            <h2>블로그에 오신 것을 환영합니다.</h2>
            <p>이곳은 Layout 컴포넌트의 본문 영역입니다.</p>
            <p>상단에는 Header, 하단에는 Footer가 표시됩니다.</p>
          </article>
        )}
      </main>
      {footer}
    </div>
  );
}

export default Layout;
