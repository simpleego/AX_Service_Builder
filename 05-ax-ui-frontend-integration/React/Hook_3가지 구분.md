# Hook의 3가지 메서드 구분
- useMemo
- useCallback
- useRef

세 훅은 기억하는 대상이 다릅니다.

| Hook | 기억하는 대상 | 대표적인 사용 목적 |
|---|---|---|
| `useMemo` | 계산 결과 | 비용이 큰 계산 반복 줄이기 |
| `useCallback` | 함수 참조 | 메모된 자식에게 동일한 함수 전달하기 |
| `useRef` | 변경 가능한 값 또는 DOM 참조 | 입력창 포커스, 타이머 ID 보관 |

아래는 **상품 검색과 장바구니** 예제입니다. React 18 프로젝트의 `App.jsx`에 넣어 실행할 수 있습니다.

```jsx
import React, {
  memo,
  useCallback,
  useMemo,
  useRef,
  useState,
} from "react";

// 렌더링마다 다시 생성하지 않는 예제 데이터
const PRODUCTS = Array.from({ length: 10000 }, (_, index) => ({
  id: index + 1,
  name: `상품 ${index + 1}`,
  price: (index + 1) * 100,
}));

// props가 같으면 부모 갱신으로 인한 렌더링을 건너뛸 수 있습니다.
const ProductList = memo(function ProductList({ products, onAdd }) {
  console.log("ProductList 렌더링");

  return (
    <ul>
      {products.slice(0, 20).map((product) => (
        <li key={product.id}>
          {product.name} / {product.price.toLocaleString()}원
          <button onClick={() => onAdd(product)}>
            담기
          </button>
        </li>
      ))}
    </ul>
  );
});

export default function App() {
  const [keyword, setKeyword] = useState("");
  const [cart, setCart] = useState([]);
  const [dark, setDark] = useState(false);

  // ① useRef: 실제 input DOM을 기억합니다.
  const inputRef = useRef(null);

  // ② useMemo: 검색 결과 배열을 기억합니다.
  const filteredProducts = useMemo(() => {
    console.log("상품 검색 계산");

    const query = keyword.trim().toLowerCase();

    return PRODUCTS.filter((product) =>
      product.name.toLowerCase().includes(query)
    );
  }, [keyword]);

  // ③ useCallback: 자식에게 전달할 함수 참조를 기억합니다.
  const handleAdd = useCallback((product) => {
    // 함수형 갱신으로 최신 장바구니를 받습니다.
    setCart((previousCart) => [...previousCart, product]);
  }, []);

  function focusSearch() {
    inputRef.current?.focus();
  }

  return (
    <main
      style={{
        padding: 24,
        backgroundColor: dark ? "#222" : "#fff",
        color: dark ? "#fff" : "#222",
      }}
    >
      <h1>상품 검색</h1>

      <label>
        검색어:
        <input
          ref={inputRef}
          value={keyword}
          onChange={(event) => setKeyword(event.target.value)}
        />
      </label>

      <button onClick={focusSearch}>
        검색창으로 이동
      </button>

      <button onClick={() => setDark((previous) => !previous)}>
        테마 변경
      </button>

      <p>장바구니: {cart.length}개</p>
      <p>검색 결과: {filteredProducts.length}개, 최대 20개 표시</p>

      <ProductList
        products={filteredProducts}
        onAdd={handleAdd}
      />
    </main>
  );
}
```

**1. `useMemo`: 검색 결과를 왜 기억해야 할까?**

상품 검색은 10,000개 데이터를 순회합니다. 일반적으로 컴포넌트 안에서 계산하면 **테마 변경이나 장바구니 추가로 부모가 렌더링될 때도 검색을 다시 수행**합니다.

```jsx
// 부모가 렌더링될 때마다 새로 계산하고 새 배열을 만듭니다.
const filteredProducts = PRODUCTS.filter(/* 검색 조건 */);
```

`useMemo`를 사용하면 `keyword`가 같을 때 이전 검색 결과를 재사용합니다. 결과 배열의 참조도 유지되어 `memo`로 감싼 `ProductList`의 렌더링 생략에 도움이 됩니다.

실제 계산이 가볍다면 생략해도 됩니다. **정확한 동작을 위한 필수 기능이 아니라 성능 최적화 도구**입니다. 계산 함수에는 API 호출이나 상태 변경을 넣지 않습니다. [공식 useMemo 문서](https://react.dev/reference/react/useMemo)

**2. `useCallback`: 함수를 왜 기억해야 할까?**

일반적인 함수 선언은 부모가 렌더링될 때마다 새로운 함수 값을 만듭니다.

```jsx
// 실행 내용은 같아도 매 렌더링에서 다른 함수 참조입니다.
const handleAdd = (product) => {
  setCart((previous) => [...previous, product]);
};
```

그러면 `ProductList`를 `memo`로 감싸도 `onAdd`가 바뀌었다고 판단하여 다시 렌더링할 수 있습니다.

`useCallback`은 의존성이 같을 때 **이전 함수 참조를 반환**합니다. 이 예제에서는 함수형 상태 갱신을 사용하므로 `cart`를 직접 읽지 않아 의존성을 `[]`로 둘 수 있습니다.

```jsx
const handleAdd = useCallback((product) => {
  setCart((previous) => [...previous, product]);
}, []);
```

이미지의 설명에 조건을 보충하면, **`useCallback`만으로 자식 렌더링이 막히지는 않습니다.** 이 예제에서는 `memo`와 함께 사용하고, 다른 prop인 `products`도 유지되도록 했습니다. 또한 함수 생성 자체를 완전히 없애는 기능은 아닙니다. [공식 useCallback 문서](https://react.dev/reference/react/useCallback)

**3. `useRef`: 입력창을 왜 기억해야 할까?**

“검색창으로 이동” 버튼은 실제 input DOM에 `focus()`를 호출해야 합니다.

```jsx
const inputRef = useRef(null);

// DOM이 연결되면 React가 current에 input 요소를 넣습니다.
<input ref={inputRef} />

// 이벤트 핸들러에서 DOM 사용
inputRef.current?.focus();
```

일반 지역 변수는 렌더마다 새로 만들어지지만, ref 객체는 렌더 사이에 유지됩니다. `.current`를 변경해도 렌더링을 요청하지 않습니다.

따라서 검색어처럼 **화면에 표시할 데이터는 `useState`**, DOM이나 타이머 ID처럼 **변경 자체로 화면을 갱신할 필요가 없는 값은 `useRef`**가 적합합니다. [공식 useRef 문서](https://react.dev/reference/react/useRef)

동작을 확인할 때는 브라우저 콘솔을 열어 다음 순서로 조작하세요.

| 조작 | 검색 계산 | ProductList 렌더링 |
|---|---|---|
| 검색어 변경 | 다시 수행 | 검색 결과가 바뀌므로 수행 |
| 테마 변경 | 이전 결과 재사용 | props가 같아 생략 가능 |
| 상품 담기 | 이전 결과 재사용 | props가 같아 생략 가능 |
| 검색창으로 이동 | 필요 없음 | 포커스만 변경 |

개발 환경의 `StrictMode`에서는 순수성 검사를 위해 초기 렌더나 계산 로그가 두 번 나타날 수 있습니다.
