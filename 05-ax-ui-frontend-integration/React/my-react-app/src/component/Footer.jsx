import React from 'react';

function Footer() {
  return (
    <footer className="site-footer">
      <small>© {new Date().getFullYear()} 소플의 블로그. React 학습 예제.</small>
    </footer>
  );
}

export default Footer;