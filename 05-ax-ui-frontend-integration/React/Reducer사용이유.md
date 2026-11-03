`useState` 대신 `useReducer`를 사용하는 핵심 이유는 "상태 변경 로직의 복잡성을 컴포넌트 외부(reducer 함수)로 분리하고, 여러 상태를 안전하게 관리하기 위해서"입니다.

실제 개발에서 `useState`보다 `useReducer`가 빛을 발하는 대표적인 이유는 다음과 같습니다.

---

### 1. 상태 변경 로직의 중앙 집중화 (관심사 분리)

* **`useState`**: 상태를 바꾸는 코드(`setCount`, `setForm` 등)가 컴포넌트 내부의 이벤트 핸들러나 여러 곳에 흩어지기 쉽습니다. 컴포넌트가 비대해지면 상태가 어떻게 변하는지 파악하기 어려워집니다.
* **`useReducer`**: 상태를 어떻게 바꿀지 정의한 **`reducer` 함수**가 컴포넌트 외부(또는 별도 파일)에 독립적으로 존재합니다. "상태를 변경하는 규칙"이 한곳에 모여 있어 코드의 가독성이 좋아지고 유지보수가 편해집니다.

### 2. 연관된 여러 상태를 한 번에 안전하게 관리 (복잡한 상태 구조)

* **`useState`**: 여러 개의 `useState`를 쓰면 상태 간의 동기화가 깨지거나 코드가 복잡해질 수 있습니다. (예: `orders`, `nextId`, `filter` 등을 각각 `useState`로 선언하면 동시에 업데이트할 때 누락이나 오류가 발생하기 쉽습니다.)
* **`useReducer`**: [주문 관리 시스템 예제](https://github.com/simpleego/AX_Service_Builder/blob/main/05-ax-ui-frontend-integration/React/useReducer%EC%98%88%EC%A0%9C.md#5-%EC%A3%BC%EB%AC%B8-%EA%B4%80%EB%A6%AC-%EC%8B%9C%EC%8A%A4%ED%85%9C--%EB%B3%B5%ED%95%A9-%EC%83%81%ED%83%9C%EC%99%80-%EC%97%85%EB%AC%B4-%EA%B7%9C%EC%B9%99)처럼 여러 속성을 가진 객체 상태를 다룰 때 유리합니다. 하나의 액션(`dispatch`)으로 여러 연관된 값을 동시에 일관성 있게 변경할 수 있습니다.
```javascript
return {
  ...state,
  orders: [...state.orders, newOrder],
  nextId: state.nextId + 1 // 연관된 상태를 한 번에 안전하게 갱신
};

```



### 3. 예측 가능성과 디버깅 용이성 (액션 기반 설계)

* **`useState`**: 값이 언제, 어디서, 왜 바뀌었는지 추적하기가 상대적으로 어렵습니다.
* **`useReducer`**: 모든 상태 변경은 반드시 `dispatch({ type: "ACTION_NAME", ... })`라는 **액션 객체**를 통해서만 일어납니다. "어떤 의도(type)로 상태가 변경되었는지" 명확하게 기록되므로, Redux DevTools 같은 도구를 쓰거나 로깅을 할 때 상태 흐름을 추적하기가 매우 쉽습니다.

### 4. 복잡한 업데이트 규칙 (조건문과 불변성 관리)

* [장바구니 예제](https://github.com/simpleego/AX_Service_Builder/blob/main/05-ax-ui-frontend-integration/React/useReducer%EC%98%88%EC%A0%9C.md#react-%EA%B5%AC%ED%98%84-%EC%BD%94%EB%93%9C--shoppingcartjsx)나 [Todo 앱](https://github.com/simpleego/AX_Service_Builder/blob/main/05-ax-ui-frontend-integration/React/useReducer%EC%98%88%EC%A0%9C.md#3-todo-%EC%95%B1--%EB%B0%B0%EC%97%B4-crud)처럼 "기존 항목이 있으면 수량을 올리고, 없으면 새로 추가한다"거나, 배열 안의 특정 아이템만 골라서 수정하는 등의 **복잡한 비즈니스 로직**이 들어갈 때 `useState`를 쓰면 코드가 장황해집니다.
* `useReducer`를 쓰면 `switch/case` 문을 통해 각 상황별 상태 변화를 명확하게 나누어 작성할 수 있습니다.

---

### 💡 요약: 언제 무엇을 써야 할까?

* **`useState`**: 단순한 숫자, 문자열, `boolean` 값 등 **단독으로 쓰이는 가벼운 상태**나 단순한 토글 등에 적합합니다.
* **`useReducer`**:
1. 관리할 상태가 **객체나 배열 형태**로 복잡할 때
2. 다음 상태가 **이전 상태에 유기적으로 의존**할 때
3. 상태 변경 로직이 복잡해서 컴포넌트 코드와 분리하고 싶을 때 (`Redux`를 본격적으로 쓰기 전 단계의 훌륭한 대안)

네, **정말 좋은 질문입니다!** 결론부터 말씀드리면 **외부 파일(.js / .jsx)로 모듈화하여 `import` 해서 사용하는 것이 실제 실무에서 가장 권장되는 표준 방식**입니다.

컴포넌트 파일 안에 `reducer` 함수와 초기 상태(`initialState`)를 함께 작성하면 코드가 길어져서 가독성이 떨어지게 됩니다. 따라서 이를 별도의 파일로 분리하면 다음과 같은 강력한 장점들이 있습니다.

---

### 1. 모듈화의 장점

* **관심사 분리(Separation of Concerns)**: UI를 렌더링하는 컴포넌트 코드와 순수 상태 변경 로직(`reducer`)이 완벽히 분리되어 코드가 깔끔해집니다.
* **단위 테스트(Unit Testing) 용이성**: `reducer` 함수는 `(state, action) => newState` 형태의 순수 함수(Pure Function)이기 때문에, UI를 렌더링하지 않고도 `reducer` 함수만 따로 떼어내어 테스트하기가 매우 쉽습니다.
* **재사용성**: 동일한 상태 관리 로직이나 액션이 여러 곳에서 필요할 때 모듈을 불러와서 재사용할 수 있습니다.

---

### 2. 실제 코드 작성 예시

#### ① 리듀서 로직 분리하기 (`cartReducer.js`)

```javascript
// src/reducers/cartReducer.js

export const initialCartState = [];

export function cartReducer(state, action) {
  switch (action.type) {
    case "ADD": {
      const product = action.product;
      const exists = state.some(item => item.id === product.id);

      if (exists) {
        return state.map(item =>
          item.id === product.id
            ? { ...item, qty: item.qty + 1 }
            : item
        );
      }

      return [...state, { ...product, qty: 1 }];
    }

    case "REMOVE":
      return state.filter(item => item.id !== action.id);

    case "CLEAR":
      return [];

    default:
      return state;
  }
}

```

#### ② 컴포넌트에서 가져와서 사용하기 (`ShoppingCart.jsx`)

```javascript
// src/components/ShoppingCart.jsx
import { useReducer } from "react";
// 방금 분리한 reducer와 초기 상태를 모듈로 임포트
import { cartReducer, initialCartState } from "../reducers/cartReducer";

const products = [
  { id: 1, name: "키보드", price: 45000 },
  { id: 2, name: "마우스", price: 25000 },
];

export default function ShoppingCart() {
  // 임포트한 함수와 상태를 그대로 전달
  const [cart, dispatch] = useReducer(cartReducer, initialCartState);

  return (
    <div>
      <h2>장바구니 실습</h2>
      {products.map(product => (
        <button 
          key={product.id} 
          onClick={() => dispatch({ type: "ADD", product })}
        >
          {product.name} 담기
        </button>
      ))}
    </div>
  );
}

```

---

이처럼 복잡한 `useReducer` 로직이나 액션 생성 함수(Action Creators)들을 별도의 모듈 파일로 관리하는 것은 리액트 프로젝트 구조를 쾌적하게 만드는 훌륭한 패턴입니다.

혹시 프로젝트 구조를 나누거나 모듈을 구성할 때 추가로 궁금한 점이 있으신가요?
