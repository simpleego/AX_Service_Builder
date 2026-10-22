// ============================================================
// 연습 08. 모듈 (import / export)
// 실행: node exercises/08-modules.js   (정답: solutions/08-modules.js)
// 이번에는 이 파일이 아니라 08-modules/cart.js 를 완성합니다.
// 이 파일은 cart.js를 불러와 채점만 합니다.
// ============================================================
import { check, summary } from '../lib/check.js';

// 파일 전체를 객체 하나로 불러온다. (아직 export가 없어도 채점이 멈추지 않도록)
import * as cart from './08-modules/cart.js';

// 문제 4. 이 파일에서 할 일: cart.js의 함수를 써서 결과를 만드세요.
//         빈 장바구니에 { name: '책', price: 10000 }, { name: '펜', price: 2000 } 을 차례로 넣고
//         세금 포함 합계를 돌려주세요. (cart.addToCart, cart.default 사용)
export function checkout() {
  // ▼
  // 여기에 코드를 작성하세요
  // ▲
}

check('1. TAX_RATE 내보내기', () => cart.TAX_RATE, 0.1);
check('2-1. addToCart 내보내기', () => typeof cart.addToCart, 'function');
check('2-2. addToCart는 새 배열', () => {
  const before = [{ name: '사과', price: 1000 }];
  const after = cart.addToCart(before, { name: '배', price: 2000 });
  return [after.length, before.length, after !== before];
}, [2, 1, true]);
check('3. default로 totalWithTax 내보내기', () => cart.default([{ price: 1000 }, { price: 2000 }]), 3300);
check('4. 계산하기', () => checkout(), 13200);
summary();

// 생각해 보기: React 파일에서 아래 두 줄의 차이는?
//   import TodoForm from './TodoForm';         ← default
//   import { useState } from 'react';          ← named
