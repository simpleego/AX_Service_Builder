# useMemo 사용 예시

`useMemo`는 **계산 결과 값을 기억해 두었다가, 의존성 값이 바뀔 때만 다시 계산하는 Hook**입니다.

컴포넌트가 다시 렌더링되면 그 안의 계산도 매번 **다시 실행됩니다**. 계산이 무겁거나, 결과로 만든 객체·배열을 자식이나 `useEffect`에 넘길 때 불필요한 작업이 생깁니다. `useMemo`는 이 문제를 막아 줍니다.

```jsx
const 기억된값 = useMemo(() => 계산해서_돌려줄_값, [의존성]);
```

대표적인 경우 6가지를 예시와 함께 정리했습니다.

---

## 1. 무거운 계산 결과 기억하기

계산에 시간이 오래 걸리면, 관련 없는 state가 바뀔 때마다 화면이 느려집니다.

```jsx
import { useState, useMemo } from 'react';

// 1부터 n까지의 소수를 구하는 무거운 계산
function getPrimes(n) {
  console.log('소수 계산 실행');
  const primes = [];
  for (let i = 2; i <= n; i++) {
    let isPrime = true;
    for (let j = 2; j * j <= i; j++) {
      if (i % j === 0) { isPrime = false; break; }
    }
    if (isPrime) primes.push(i);
  }
  return primes;
}

function PrimeCounter() {
  const [limit, setLimit] = useState(100000);
  const [dark, setDark] = useState(false);

  // limit이 바뀔 때만 다시 계산합니다 (테마를 바꿀 때는 계산하지 않음)
  const primes = useMemo(() => getPrimes(limit), [limit]);

  return (
    <div style={{ background: dark ? '#222' : '#fff', color: dark ? '#fff' : '#000' }}>
      <input type="number" value={limit} onChange={e => setLimit(Number(e.target.value))} />
      <p>소수 개수: {primes.length}</p>
      <button onClick={() => setDark(d => !d)}>테마 전환</button>
    </div>
  );
}
```

## 2. 목록 검색과 정렬

검색어나 정렬 기준이 바뀔 때만 목록을 다시 거릅니다.

```jsx
import { useState, useMemo } from 'react';

function ProductTable({ products }) {
  const [keyword, setKeyword] = useState('');
  const [sortBy, setSortBy] = useState('name');
  const [selectedId, setSelectedId] = useState(null);

  // 행을 선택할 때(selectedId 변경)는 다시 거르지 않습니다
  const visibleProducts = useMemo(() => {
    console.log('필터링 + 정렬 실행');
    return products
      .filter(p => p.name.toLowerCase().includes(keyword.toLowerCase()))
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
```

> `.sort()`는 원본 배열을 바꾸지만, 여기서는 `.filter()`가 새 배열을 먼저 만들어서 props로 받은 `products`는 그대로입니다.

## 3. 합계·통계 값 계산하기 (장바구니)

목록에서 합계, 개수, 평균 같은 값을 뽑아낼 때 씁니다.

```jsx
import { useState, useMemo } from 'react';

function Cart() {
  const [items, setItems] = useState([
    { id: 1, name: '키보드', price: 50000, qty: 1 },
    { id: 2, name: '마우스', price: 25000, qty: 2 },
  ]);
  const [coupon, setCoupon] = useState('');

  const summary = useMemo(() => {
    const totalQty = items.reduce((sum, item) => sum + item.qty, 0);
    const totalPrice = items.reduce((sum, item) => sum + item.price * item.qty, 0);
    const shipping = totalPrice >= 50000 ? 0 : 3000;
    return { totalQty, totalPrice, shipping, payment: totalPrice + shipping };
  }, [items]); // 쿠폰을 입력할 때는 다시 계산하지 않습니다

  const increase = (id) =>
    setItems(prev => prev.map(item => (item.id === id ? { ...item, qty: item.qty + 1 } : item)));

  return (
    <div>
      {items.map(item => (
        <p key={item.id}>
          {item.name} x {item.qty} <button onClick={() => increase(item.id)}>+</button>
        </p>
      ))}
      <input value={coupon} onChange={e => setCoupon(e.target.value)} placeholder="쿠폰 코드" />
      <p>총 {summary.totalQty}개 / 상품 금액 {summary.totalPrice.toLocaleString()}원</p>
      <p>배송비 {summary.shipping.toLocaleString()}원</p>
      <h3>결제 금액 {summary.payment.toLocaleString()}원</h3>
    </div>
  );
}
```

## 4. useEffect 의존성에 객체를 쓸 때

객체는 렌더링할 때마다 새로 만들어져서, 내용이 같아도 `useEffect`가 매번 다시 실행됩니다. `useMemo`로 감싸면 실제 값이 바뀔 때만 실행됩니다.

```jsx
import { useState, useEffect, useMemo } from 'react';

function UserSearch() {
  const [name, setName] = useState('');
  const [page, setPage] = useState(1);
  const [count, setCount] = useState(0);
  const [result, setResult] = useState([]);

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
```

> 이 예시처럼 객체 안의 값이 단순하다면, 의존성 배열에 `[name, page]`를 직접 넣는 방법이 더 간단합니다.

## 5. memo로 감싼 자식에게 배열·객체를 넘길 때

`memo`는 props가 같으면 자식을 다시 그리지 않습니다. 하지만 배열이나 객체를 렌더링 중에 새로 만들면 매번 "다른 값"이 되어 소용이 없습니다.

```jsx
import { useState, useMemo, memo } from 'react';

function Dashboard({ sales }) {
  const [note, setNote] = useState('');

  // sales가 바뀔 때만 새 배열을 만듭니다
  const chartData = useMemo(
    () => sales.map(s => ({ label: s.month, value: s.amount / 10000 })),
    [sales]
  );

  return (
    <div>
      <textarea value={note} onChange={e => setNote(e.target.value)} placeholder="메모" />
      <SalesChart data={chartData} />
    </div>
  );
}

const SalesChart = memo(({ data }) => {
  console.log('차트 렌더링'); // 메모를 입력할 때는 찍히지 않습니다
  return (
    <ul>
      {data.map(d => <li key={d.label}>{d.label}: {d.value}만원</li>)}
    </ul>
  );
});
```

## 6. Context의 value 객체 고정하기

Provider의 `value`가 바뀌면 그 Context를 쓰는 모든 컴포넌트가 다시 렌더링됩니다. value 객체를 `useMemo`로 감싸서 실제 값이 바뀔 때만 새로 만듭니다.

```jsx
import { createContext, useContext, useState, useMemo } from 'react';

const AuthContext = createContext(null);

function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [theme, setTheme] = useState('light');

  // user가 바뀔 때만 새 객체를 만듭니다
  const authValue = useMemo(
    () => ({
      user,
      isLoggedIn: user !== null,
      login: (name) => setUser({ name }),
      logout: () => setUser(null),
    }),
    [user]
  );

  return (
    <AuthContext.Provider value={authValue}>
      <button onClick={() => setTheme(t => (t === 'light' ? 'dark' : 'light'))}>
        테마: {theme}
      </button>
      {children}
    </AuthContext.Provider>
  );
}

function UserMenu() {
  const { user, isLoggedIn, login, logout } = useContext(AuthContext);
  return isLoggedIn ? (
    <p>{user.name}님 <button onClick={logout}>로그아웃</button></p>
  ) : (
    <button onClick={() => login('철수')}>로그인</button>
  );
}
```

> `setUser`는 React가 항상 같은 함수로 유지하므로 의존성에 넣지 않아도 됩니다.

---

## 정리

| 경우 | 기억하는 값 | 의존성 배열 |
|---|---|---|
| 무거운 계산 | 소수 목록 | `[limit]` |
| 검색·정렬 | 걸러진 목록 | `[products, keyword, sortBy]` |
| 합계·통계 | 합계 객체 | `[items]` |
| useEffect 의존성 | 요청 파라미터 객체 | `[name, page]` |
| memo 자식에 전달 | 차트 데이터 배열 | `[sales]` |
| Context value | value 객체 | `[user]` |

## useMemo와 useCallback 비교

| 구분 | useMemo | useCallback |
|---|---|---|
| 기억하는 것 | 함수를 **실행한 결과 값** | **함수 자체** |
| 형태 | `useMemo(() => 값, deps)` | `useCallback(fn, deps)` |
| 주 용도 | 무거운 계산, 객체·배열 고정 | 자식에게 넘길 함수 고정 |

## useMemo가 필요 없는 경우

- **가벼운 계산**(`a + b`, 짧은 문자열 연결, 몇 개짜리 배열 처리)은 그냥 계산하는 편이 더 빠르고 읽기 쉽습니다.
- **원시 값(숫자, 문자열, boolean)** 은 내용이 같으면 같은 값으로 비교되므로, 의존성 문제 때문에 감쌀 필요가 없습니다.
- `useMemo`는 성능 최적화용입니다. **없어도 결과가 같아야 합니다.** 결과가 달라진다면 코드에 다른 문제가 있는 것입니다.
- 계산이 정말 무거운지 궁금하면 `console.time('계산')` / `console.timeEnd('계산')`으로 재 보고, 1ms 이상일 때 쓰는 것을 고려합니다.
- React Compiler를 쓰는 프로젝트는 컴파일러가 자동으로 메모이제이션하므로 직접 쓸 일이 크게 줄어듭니다.
