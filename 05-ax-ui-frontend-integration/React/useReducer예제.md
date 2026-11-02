# React useReducer 실습 예제 5가지

React의 `useReducer`를 이해하기 위해 간단한 상태 변경 → 객체 상태 관리 → 배열 CRUD → 복합 상태 관리 순서로 구성했습니다.

모든 예제는 React 함수 컴포넌트로 작성하며, `useReducer` 외의 Hook 사용을 최소화하여 상태 관리 원리에 집중하도록 하겠습니다.

## 실습 구성

| 단계 | 프로젝트      | 핵심 학습 내용          | 난이도 |
| -- | --------- | ----------------- | --- |
| 1  | 카운터       | 증가·감소·초기화         | ★☆☆ |
| 2  | 로그인 폼     | 객체 상태·입력값 변경      | ★☆☆ |
| 3  | Todo 앱    | 배열 추가·삭제·완료 처리    | ★★☆ |
| 4  | 쇼핑몰 장바구니  | 상품 추가·수량 변경·합계 계산 | ★★★ |
| 5  | 주문 관리 시스템 | 복합 상태·주문 상태 전환    | ★★★ |

## 1. 카운터 — 가장 기본적인 useReducer

학습 목표: action의 `type`에 따라 상태를 변경하는 원리 이해

```
import { useReducer } from "react";

function reducer(state, action) {
  switch (action.type) {
    case "INCREMENT":
      return state + 1;
    case "DECREMENT":
      return state - 1;
    case "RESET":
      return 0;
    default:
      return state;
  }
}

export default function Counter() {
  const [count, dispatch] = useReducer(reducer, 0);

  return (
    <div>
      <h2>카운터: {count}</h2>

      <button onClick={() => dispatch({ type: "INCREMENT" })}>
        + 증가
      </button>

      <button onClick={() => dispatch({ type: "DECREMENT" })}>
        - 감소
      </button>

      <button onClick={() => dispatch({ type: "RESET" })}>
        초기화
      </button>
    </div>
  );
}
```

핵심 원리

- `state`는 현재 카운터 값입니다.
- `dispatch()`는 변경 요청을 전달합니다.
- `action.type`에 따라 reducer가 새로운 값을 계산합니다.
- reducer가 반환한 값이 새로운 state가 됩니다.

## 2. 로그인 폼 — 객체 상태 관리

학습 목표: 여러 입력값을 하나의 객체로 관리하고, action에 데이터를 전달하기

```
import { useReducer } from "react";

const initialState = {
  email: "",
  password: "",
  showPassword: false,
};

function reducer(state, action) {
  switch (action.type) {
    case "CHANGE":
      return {
        ...state,
        [action.field]: action.value,
      };

    case "TOGGLE_PASSWORD":
      return {
        ...state,
        showPassword: !state.showPassword,
      };

    case "RESET":
      return initialState;

    default:
      return state;
  }
}

export default function LoginForm() {
  const [form, dispatch] = useReducer(reducer, initialState);

  return (
    <div>
      <h2>로그인 폼</h2>

      <input
        type="email"
        placeholder="이메일"
        value={form.email}
        onChange={(e) =>
          dispatch({
            type: "CHANGE",
            field: "email",
            value: e.target.value,
          })
        }
      />

      <input
        type={form.showPassword ? "text" : "password"}
        placeholder="비밀번호"
        value={form.password}
        onChange={(e) =>
          dispatch({
            type: "CHANGE",
            field: "password",
            value: e.target.value,
          })
        }
      />

      <button onClick={() => dispatch({ type: "TOGGLE_PASSWORD" })}>
        비밀번호 표시/숨기기
      </button>

      <button onClick={() => dispatch({ type: "RESET" })}>
        초기화
      </button>

      <p>입력한 이메일: {form.email}</p>
    </div>
  );
}
```

`...state`는 기존 객체의 속성을 유지하면서 일부 속성만 변경하기 위한 전개 구문입니다.

특히 `[action.field]`는 변경할 속성 이름을 동적으로 지정합니다.

```
dispatch({
  type: "CHANGE",
  field: "email",
  value: "test@example.com",
});
```

이 요청은 `email` 속성만 변경하고 나머지 속성은 그대로 유지합니다. 비밀번호는 화면에 출력하지 않으며, 실제 로그인 인증은 수행하지 않는 입력 상태 관리 실습입니다.

## 3. Todo 앱 — 배열 CRUD

학습 목표: 배열 상태에 항목 추가·삭제·완료 상태 변경하기

```
import { useReducer, useState } from "react";

const initialTodos = [
  { id: 1, text: "React 공부", done: false },
  { id: 2, text: "useReducer 실습", done: true },
];

function reducer(state, action) {
  switch (action.type) {
    case "ADD":
      return [
        ...state,
        {
          id: action.id,
          text: action.text,
          done: false,
        },
      ];

    case "TOGGLE":
      return state.map((todo) =>
        todo.id === action.id
          ? { ...todo, done: !todo.done }
          : todo
      );

    case "DELETE":
      return state.filter((todo) => todo.id !== action.id);

    case "CLEAR_COMPLETED":
      return state.filter((todo) => !todo.done);

    default:
      return state;
  }
}

export default function TodoApp() {
  const [todos, dispatch] = useReducer(reducer, initialTodos);
  const [text, setText] = useState("");

  function handleAdd() {
    const value = text.trim();
    if (!value) return;

    dispatch({
      type: "ADD",
      id: crypto.randomUUID(),
      text: value,
    });

    setText("");
  }

  return (
    <div>
      <h2>Todo 앱</h2>

      <input
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="할 일 입력"
      />

      <button onClick={handleAdd}>추가</button>

      <ul>
        {todos.map((todo) => (
          <li key={todo.id}>
            <input
              type="checkbox"
              checked={todo.done}
              onChange={() =>
                dispatch({ type: "TOGGLE", id: todo.id })
              }
            />

            <span
              style={{
                textDecoration: todo.done ? "line-through" : "none",
              }}
            >
              {todo.text}
            </span>

            <button
              onClick={() =>
                dispatch({ type: "DELETE", id: todo.id })
              }
            >
              삭제
            </button>
          </li>
        ))}
      </ul>

      <button onClick={() => dispatch({ type: "CLEAR_COMPLETED" })}>
        완료 항목 삭제
      </button>

      <p>전체: {todos.length}개</p>
    </div>
  );
}
```

이 예제는 `useState`와 `useReducer`를 함께 사용하는 방법도 보여줍니다.

- `useState`: 단순한 입력창 상태
- `useReducer`: 여러 변경 규칙이 필요한 Todo 목록 상태

특히 `map()`과 `filter()`로 기존 배열을 직접 변경하지 않고 새로운 배열을 반환한다는 점이 중요합니다.

## 4. 쇼핑몰 장바구니 — 상품 추가·수량 변경·합계 계산

학습 목표: 여러 상품을 배열로 관리하고, 수량 및 총액을 계산하기

이번 예제에서는 쇼핑몰에 필요한 다음 기능을 구현합니다.

- 상품을 장바구니에 추가
- 같은 상품을 다시 추가하면 수량 증가
- 상품 수량 증가·감소
- 상품 삭제 및 장바구니 비우기
- 상품의 총수량과 결제 금액 계산

## 미니 쇼핑몰 체험

키보드

45,000원

담기

마우스

25,000원

담기

모니터

220,000원

담기

장바구니

담긴 상품이 없습니다.

총 수량

0개

총 결제 금액

## 0원

장바구니 비우기위 체험은 동일한 기능을 보여 주는 예시입니다. 아래 코드에서는 상태 관리에 실제 useReducer를 사용합니다.

### React 구현 코드 — ShoppingCart.jsx

```
import { useReducer } from "react";

const products = [
  { id: 1, name: "키보드", price: 45000 },
  { id: 2, name: "마우스", price: 25000 },
  { id: 3, name: "모니터", price: 220000 },
];

// 상태 변경을 처리하는 reducer
function cartReducer(state, action) {
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

    case "INCREASE":
      return state.map(item =>
        item.id === action.id
          ? { ...item, qty: item.qty + 1 }
          : item
      );

    case "DECREASE":
      return state.map(item =>
        item.id === action.id
          ? { ...item, qty: Math.max(1, item.qty - 1) }
          : item
      );

    case "REMOVE":
      return state.filter(item => item.id !== action.id);

    case "CLEAR":
      return [];

    default:
      return state;
  }
}

export default function ShoppingCart() {
  const [cart, dispatch] = useReducer(cartReducer, []);

  const total = cart.reduce(
    (sum, item) => sum + item.price * item.qty,
    0
  );

  return (
    <div>
      <h2>상품 목록</h2>

      {products.map(product => (
        <div key={product.id}>
          <span>
            {product.name} - {product.price.toLocaleString()}원
          </span>

          <button onClick={() =>
            dispatch({ type: "ADD", product })
          }>
            장바구니 담기
          </button>
        </div>
      ))}

      <hr />

      <h2>장바구니</h2>

      {cart.map(item => (
        <div key={item.id}>
          <span>{item.name} ({item.qty}개)</span>

          <button onClick={() =>
            dispatch({ type: "INCREASE", id: item.id })
          }>+</button>

          <button onClick={() =>
            dispatch({ type: "DECREASE", id: item.id })
          }>-</button>

          <button onClick={() =>
            dispatch({ type: "REMOVE", id: item.id })
          }>삭제</button>
        </div>
      ))}

      <h3>총 결제금액: {total.toLocaleString()}원</h3>

      <button onClick={() => dispatch({ type: "CLEAR" })}>
        장바구니 비우기
      </button>
    </div>
  );
}
```

### 학습 포인트

이 예제에서 중요한 부분은 동일한 상품을 중복으로 담았을 때의 처리입니다.

```
case "ADD":
```

- 상품이 없으면 새로운 상품 객체를 배열에 추가합니다.
- 상품이 이미 있으면 해당 상품의 `qty`만 1 증가시킵니다.
- 모든 처리는 기존 상태를 직접 변경하지 않고 새로운 배열을 반환합니다.

`total`은 별도의 상태로 보관하지 않고 `cart`에서 계산합니다. 이러한 값을 파생 상태(Derived State) 라고 하며, 불필요한 상태 중복을 줄이는 데 유용합니다.

## 5. 주문 관리 시스템 — 복합 상태와 업무 규칙

학습 목표: 하나의 객체 안에 여러 상태를 저장하고, 정해진 업무 규칙에 따라 변경하기

이번에는 주문 관리 시스템을 구현하겠습니다. 쇼핑몰 장바구니보다 상태 구조가 조금 더 복잡합니다.

주문에는 다음과 같은 정보가 있다고 가정합니다.

```
{
  orders: [],      // 주문 목록
  nextId: 1,       // 다음 주문 번호
  filter: "ALL"    // 주문 목록 필터
}
```

주문 상태는 `접수 → 배송 중 → 배송 완료` 순서로 변경됩니다.

### React 구현 코드 — OrderManager.jsx

```
import { useReducer } from "react";

const initialState = {
  orders: [],
  nextId: 1,
  filter: "ALL",
};

function orderReducer(state, action) {
  switch (action.type) {
    case "ADD_ORDER":
      return {
        ...state,
        orders: [
          ...state.orders,
          {
            id: state.nextId,
            product: action.product,
            status: "접수",
          },
        ],
        nextId: state.nextId + 1,
      };

    case "NEXT_STATUS":
      return {
        ...state,
        orders: state.orders.map(order => {
          if (order.id !== action.id) return order;

          const next = {
            "접수": "배송 중",
            "배송 중": "배송 완료",
            "배송 완료": "배송 완료",
          };

          return {
            ...order,
            status: next[order.status],
          };
        }),
      };

    case "DELETE_ORDER":
      return {
        ...state,
        orders: state.orders.filter(
          order => order.id !== action.id
        ),
      };

    case "SET_FILTER":
      return {
        ...state,
        filter: action.filter,
      };

    case "RESET":
      return initialState;

    default:
      return state;
  }
}

export default function OrderManager() {
  const [state, dispatch] = useReducer(
    orderReducer,
    initialState
  );

  const visibleOrders = state.orders.filter(order =>
    state.filter === "ALL" || order.status === state.filter
  );

  return (
    <div>
      <h2>주문 관리 시스템</h2>

      <button onClick={() =>
        dispatch({
          type: "ADD_ORDER",
          product: "노트북",
        })
      }>
        노트북 주문
      </button>

      <button onClick={() =>
        dispatch({
          type: "ADD_ORDER",
          product: "모니터",
        })
      }>
        모니터 주문
      </button>

      <hr />

      <select
        value={state.filter}
        onChange={e =>
          dispatch({
            type: "SET_FILTER",
            filter: e.target.value,
          })
        }
      >
        <option value="ALL">전체</option>
        <option value="접수">접수</option>
        <option value="배송 중">배송 중</option>
        <option value="배송 완료">배송 완료</option>
      </select>

      <h3>주문 목록 ({visibleOrders.length}건)</h3>

      {visibleOrders.map(order => (
        <div key={order.id}>
          <span>
            #{order.id} {order.product} - {order.status}
          </span>

          <button
            disabled={order.status === "배송 완료"}
            onClick={() =>
              dispatch({
                type: "NEXT_STATUS",
                id: order.id,
              })
            }
          >
            다음 단계
          </button>

          <button onClick={() =>
            dispatch({
              type: "DELETE_ORDER",
              id: order.id,
            })
          }>
            삭제
          </button>
        </div>
      ))}

      <p>전체 주문 수: {state.orders.length}</p>

      <button onClick={() => dispatch({ type: "RESET" })}>
        전체 초기화
      </button>
    </div>
  );
}
```

### 학습 포인트

이 예제에서는 `state`가 단순한 숫자나 배열이 아니라 여러 속성을 가진 객체입니다.

예를 들어 아래 코드는 주문 목록과 다음 주문 번호를 한 번에 변경합니다.

```
return {
  ...state,
  orders: [...state.orders, newOrder],
  nextId: state.nextId + 1
};
```

이처럼 서로 연관된 여러 상태를 일관성 있게 변경해야 할 때 `useReducer`가 특히 유용합니다.

또한 주문 상태를 변경하는 규칙이 reducer에 집중되어 있으므로, 나중에 `취소`, `반품`, `환불`과 같은 업무 상태가 추가되어도 변경 로직을 체계적으로 관리할 수 있습니다.

## 6. 5개 예제를 하나의 React 프로젝트에서 실행하기

Vite를 이용하면 5개 실습을 하나의 프로젝트로 구성할 수 있습니다.

### 프로젝트 생성

```
npm create vite@latest reducer-practice -- --template react
cd reducer-practice
npm install
npm run dev
```

### 폴더 구조

```
reducer-practice/
├── src/
│   ├── examples/
│   │   ├── Counter.jsx
│   │   ├── LoginForm.jsx
│   │   ├── TodoApp.jsx
│   │   ├── ShoppingCart.jsx
│   │   └── OrderManager.jsx
│   ├── App.jsx
│   └── main.jsx
└── package.json
```

### App.jsx

아래처럼 5개 컴포넌트를 등록하면 한 화면에서 모두 실행할 수 있습니다.

```
import Counter from "./examples/Counter";
import LoginForm from "./examples/LoginForm";
import TodoApp from "./examples/TodoApp";
import ShoppingCart from "./examples/ShoppingCart";
import OrderManager from "./examples/OrderManager";

export default function App() {
  return (
    <main>
      <h1>useReducer 실습</h1>

      <section><Counter /></section>
      <hr />

      <section><LoginForm /></section>
      <hr />

      <section><TodoApp /></section>
      <hr />

      <section><ShoppingCart /></section>
      <hr />

      <section><OrderManager /></section>
    </main>
  );
}
```

## 7. 입문자가 반드시 이해해야 할 4가지

| 구성 요소      | 의미              | 예시                         |
| ---------- | --------------- | -------------------------- |
| `state`    | 현재 저장된 상태       | 장바구니 배열                    |
| `action`   | 변경 요청 정보        | `{type: "REMOVE", id: 1}`  |
| `dispatch` | 변경 요청 전달 함수     | `dispatch(action)`         |
| `reducer`  | 새로운 상태를 계산하는 함수 | `return state.filter(...)` |

특히 다음 두 가지를 강조해서 지도하는 것을 권장합니다.

첫째, reducer는 상태를 직접 변경하지 않습니다.

```
// 잘못된 예시
state.push(newItem);
return state;

// 올바른 예시
return [...state, newItem];
```

둘째, reducer는 순수 함수로 작성해야 합니다. 동일한 `state`와 `action`이 전달되면 동일한 결과를 반환해야 합니다. API 요청, 화면 알림, 난수 생성 등 부수 효과는 reducer 외부에서 처리합니다.

학습 순서로는 카운터 → 로그인 폼 → Todo → 장바구니 → 주문 관리를 추천합니다. 3번 Todo부터 `useState`로 먼저 구현한 다음 `useReducer`로 변환해 보면, 두 Hook의 구조적 차이와 사용 목적을 더욱 분명하게 이해할 수 있습니다.
