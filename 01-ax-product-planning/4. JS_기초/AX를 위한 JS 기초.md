AX(AI 전환) 기반 웹서비스 개발을 기준으로 보면, 자바스크립트는 **사용자의 입력을 받고 → 백엔드·AI에 요청하고 → 결과를 화면에 보여주는 역할**을 합니다.

비전공자라면 문법 전체를 외우기보다 **AI가 작성한 코드를 읽고, 수정하고, 정상 동작을 확인하는 데 필요한 핵심**부터 익히는 것이 좋습니다.

**1. 먼저 알아야 할 학습 범위**

| 핵심 내용   | 알아야 할 문법·기능                             | 쇼핑몰·AI 서비스 활용           |
| ------- | --------------------------------------- | ----------------------- |
| 변수와 자료형 | `const`, `let`, 문자열·숫자·불리언              | 상품명, 가격, 로그인 여부 저장      |
| 조건문     | `if`, 비교·논리 연산자                         | 재고 확인, 입력값 검사           |
| 배열과 객체  | `[]`, `{}`, 속성 접근                       | 상품 목록, 사용자 정보, AI 응답 관리 |
| 함수      | 일반 함수, 화살표 함수                           | 금액 계산, 요청 처리 기능 분리      |
| 배열 처리   | `forEach`, `map`, `filter`, `find`      | 상품 출력·검색·선택             |
| 화면 조작   | `querySelector`, `textContent`, `value` | 입력값 읽기, 결과 표시           |
| 이벤트     | `addEventListener`                      | 클릭·검색·폼 제출 처리           |
| 비동기·API | `async`, `await`, `fetch`, `try/catch`  | 백엔드·AI 호출               |
| 데이터 전달  | JSON, 구조 분해, 전개 연산자                     | 요청·응답 처리, 데이터 갱신        |

---

**2. 변수·자료형·조건문: 데이터를 저장하고 판단하기**

기본은 `const`를 사용하고, **값을 다시 대입해야 할 때만 `let`**을 사용합니다.

```javascript
const productName = "무선 마우스"; // 문자열
const price = 25000;             // 숫자
const isMember = true;           // 불리언
let quantity = 2;                // 변경 가능한 값

quantity = 3;

const totalPrice = price * quantity;

if (isMember && totalPrice >= 50000) {
    console.log("무료 배송입니다.");
} else {
    console.log("배송비가 추가됩니다.");
}
```

자주 사용하는 연산자는 다음과 같습니다.

| 연산자                  | 의미         | 예시                                |              |          |   |          |
| -------------------- | ---------- | --------------------------------- | ------------ | -------- | - | -------- |
| `+ - * / %`          | 산술 계산      | `price * quantity`                |              |          |   |          |
| `===`, `!==`         | 같은지·다른지 비교 | `status === "완료"`                 |              |          |   |          |
| `>`, `>=`, `<`, `<=` | 크기 비교      | `stock > 0`                       |              |          |   |          |
| `&&`                 | 두 조건 모두 만족 | `isMember && totalPrice >= 50000` |              |          |   |          |
| `                    |            | `                                 | 하나 이상의 조건 만족 | `isAdmin |   | isOwner` |
| `!`                  | 참·거짓 반전    | `!isLoading`                      |              |          |   |          |

특히 **HTML 입력값은 기본적으로 문자열**이므로 계산 전에 숫자로 변환해야 합니다.

```javascript
const quantity = Number("3");

console.log(quantity + 1); // 4
console.log("3" + 1);      // "31"
```

---

**3. 배열·객체: 서비스 데이터를 표현하기**

**객체는 하나의 정보 묶음**, **배열은 여러 데이터를 담는 목록**입니다.

```javascript
// 객체: 상품 하나
const product = {
    id: 1,
    name: "무선 마우스",
    price: 25000,
    stock: 10
};

console.log(product.name);  // 무선 마우스
console.log(product.price); // 25000

// 배열: 여러 상품
const products = [
    { id: 1, name: "무선 마우스", price: 25000 },
    { id: 2, name: "키보드", price: 45000 },
    { id: 3, name: "모니터", price: 200000 }
];

console.log(products[0].name); // 무선 마우스
```

백엔드와 AI 서비스에서 전달받는 데이터도 이러한 **객체와 배열의 조합**으로 다루는 경우가 많습니다.

배열에서는 다음 네 가지를 우선 익히면 됩니다.

```javascript
// forEach: 각각에 대해 작업하기
products.forEach(product => {
    console.log(product.name);
});

// map: 각 항목을 변환하여 새 배열 만들기
const names = products.map(product => product.name);
// ["무선 마우스", "키보드", "모니터"]

// filter: 조건에 맞는 항목들을 새 배열로 만들기
const affordableProducts = products.filter(
    product => product.price <= 50000
);

// find: 조건에 맞는 첫 번째 항목 찾기
const selectedProduct = products.find(
    product => product.id === 2
);
```

> `map`은 **변환**, `filter`는 **여러 개 추리기**, `find`는 **하나 찾기**로 이해하면 쉽습니다. `find`는 결과가 없으면 `undefined`를 반환합니다.

---

**4. 함수: 반복되는 작업에 이름 붙이기**

함수는 **입력값을 받아 작업하고, 필요한 결과를 돌려주는 코드 묶음**입니다.

```javascript
function calculateTotal(price, quantity) {
    return price * quantity;
}

const total = calculateTotal(25000, 3);

console.log(total); // 75000
```

AI가 생성한 코드나 프론트엔드 코드에는 화살표 함수도 자주 등장합니다.

```javascript
const calculateTotal = (price, quantity) => {
    return price * quantity;
};

// 결과를 바로 반환하면 축약 가능
const calculateTotalShort = (price, quantity) => price * quantity;
```

처음에는 **일반 함수로 입력·처리·반환을 이해하고, 화살표 함수 표현을 추가로 익히는 순서**가 좋습니다.

---

**5. DOM·이벤트: 화면과 자바스크립트 연결하기**

DOM은 자바스크립트가 HTML 요소를 찾아 읽거나 변경할 수 있게 하는 구조입니다.

다음 예시는 입력한 이름을 화면에 표시합니다.

```html
<input id="nameInput" type="text" placeholder="이름 입력">
<button id="greetButton" type="button">인사하기</button>
<p id="result"></p>

<script>
    // HTML 요소 찾기
    const input = document.querySelector("#nameInput");
    const button = document.querySelector("#greetButton");
    const result = document.querySelector("#result");

    // 클릭했을 때 실행할 작업 등록
    button.addEventListener("click", () => {
        const name = input.value.trim();

        if (name === "") {
            result.textContent = "이름을 입력하세요.";
            return;
        }

        result.textContent = `${name}님, 안녕하세요.`;
    });
</script>
```

| 표현                               | 역할             |
| -------------------------------- | -------------- |
| `querySelector("#nameInput")`    | 해당 HTML 요소 찾기  |
| `input.value`                    | 입력창의 값 읽기      |
| `trim()`                         | 문자열 양쪽 공백 제거   |
| `addEventListener("click", ...)` | 클릭 시 실행할 함수 등록 |
| `textContent`                    | 요소의 텍스트 변경     |
| `` `${name}님` ``                 | 문자열 안에 변수 넣기   |

**사용자 입력이나 AI 답변을 일반 텍스트로 표시할 때는 `textContent`를 사용**하는 것이 좋습니다. `innerHTML`은 문자열을 HTML로 해석하므로, 검증되지 않은 내용을 넣으면 보안 문제가 생길 수 있습니다.

---

**6. 비동기·API: 백엔드와 AI 연결하기**

AX 서비스에서 특히 중요한 부분입니다.

**API 응답은 시간이 걸리므로, 응답을 기다린 뒤 결과를 처리하는 방식**이 필요합니다.

| 기능                | 쉬운 설명                            |
| ----------------- | -------------------------------- |
| `fetch()`         | 서버에 요청 보내기                       |
| `async`           | 비동기 작업을 처리하는 함수 선언               |
| `await`           | 해당 비동기 작업이 끝날 때까지 함수의 다음 단계 기다리기 |
| `response.ok`     | HTTP 응답의 성공 여부 확인                |
| `response.json()` | 응답의 JSON 본문을 자바스크립트 값으로 변환       |
| `try/catch`       | 작업 중 발생한 오류 처리                   |
| `finally`         | 성공·실패와 관계없이 마무리 작업 실행            |

다음은 **질문을 백엔드에 보내고 AI 답변을 표시하는 프론트엔드 예시**입니다.

백엔드에 `POST /api/chat`이 구현되어 있고, 응답이 `{"answer": "답변 내용"}` 형식이라고 가정합니다.

```html
<form id="chatForm">
    <input
        id="question"
        type="text"
        placeholder="질문을 입력하세요"
        required
    >
    <button id="sendButton" type="submit">질문하기</button>
</form>

<p id="answer" aria-live="polite"></p>

<script>
    const form = document.querySelector("#chatForm");
    const questionInput = document.querySelector("#question");
    const sendButton = document.querySelector("#sendButton");
    const answer = document.querySelector("#answer");

    form.addEventListener("submit", async (event) => {
        // 폼 제출로 페이지가 새로고침되는 기본 동작 방지
        event.preventDefault();

        const question = questionInput.value.trim();

        if (question === "") {
            answer.textContent = "질문을 입력하세요.";
            return;
        }

        sendButton.disabled = true;
        answer.textContent = "답변을 생성하고 있습니다.";

        try {
            const response = await fetch("/api/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ question: question })
            });

            // fetch는 400·500 등의 HTTP 오류만으로 예외를 던지지 않음
            if (!response.ok) {
                throw new Error(`서버 오류: ${response.status}`);
            }

            const data = await response.json();

            if (typeof data.answer !== "string") {
                throw new Error("응답 형식이 올바르지 않습니다.");
            }

            answer.textContent = data.answer;

        } catch (error) {
            console.error(error);
            answer.textContent = "요청에 실패했습니다. 다시 시도하세요.";

        } finally {
            sendButton.disabled = false;
        }
    });
</script>
```

이 예시에서 이해해야 할 흐름은 다음과 같습니다.

1. 입력값을 읽고 빈 질문인지 검사합니다.
2. 버튼을 비활성화하고 처리 중임을 표시합니다.
3. 백엔드에 질문을 전송합니다.
4. 응답을 확인하고 답변을 표시합니다.
5. 실패하면 오류 안내를 표시합니다.
6. 버튼을 다시 활성화합니다.

**AI API의 비밀 키는 브라우저 코드에 넣지 않고 백엔드에서 관리해야 합니다.** 위 코드처럼 프론트엔드는 자신의 백엔드에 요청하도록 구성합니다.

---

**7. AI 생성 코드를 읽기 위해 추가로 알아둘 표현**

| 표현                  | 의미                                | 예시                                             |
| ------------------- | --------------------------------- | ---------------------------------------------- |
| 구조 분해               | 객체·배열에서 값을 꺼내 변수로 저장              | `const { name, price } = product;`             |
| 전개 연산자              | 객체·배열을 펼쳐 얕게 복사하거나 결합             | `const copy = { ...product };`                 |
| 삼항 연산자              | 조건에 따라 값 선택                       | `stock > 0 ? "구매 가능" : "품절"`                   |
| 선택적 체이닝             | 중간 값이 `null`·`undefined`이면 접근을 멈춤 | `user?.address?.city`                          |
| 널 병합 연산자            | 값이 `null`·`undefined`이면 기본값 사용    | `data.answer ?? "답변 없음"`                       |
| `import` / `export` | 파일 사이에서 함수·값 공유                   | `import { calculateTotal } from "./utils.js";` |

특히 객체를 수정하는 다음 두 방식의 차이를 이해하면 React 학습에도 도움이 됩니다.

```javascript
// 기존 객체의 값을 직접 변경
product.price = 30000;

// 기존 객체를 기반으로 새 객체 생성
const updatedProduct = {
    ...product,
    price: 30000
};
```

`const`는 **변수에 다른 값을 다시 대입하지 못하게 할 뿐**, 객체 내부 속성의 변경까지 막지는 않습니다.

**학습 완료 기준은 “작은 API 연동 화면을 설명하고 수정할 수 있는가”입니다.** 상품 검색이나 AI 질문 화면 하나를 만들면서 입력 검사, 배열 처리, 이벤트, 서버 요청, 로딩·오류 표시까지 연결하면 AX 웹서비스 개발에 필요한 자바스크립트의 기본 흐름을 익힐 수 있습니다.
