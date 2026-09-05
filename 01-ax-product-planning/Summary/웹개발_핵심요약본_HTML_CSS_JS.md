# 웹개발 핵심 요약본 — HTML · CSS · JavaScript

> **대상**: 풀스택 웹개발을 처음 배우는 비전공자
> **목표**: AI 도구를 활용하더라도 반드시 이해하고 있어야 하는 웹개발의 핵심 개념 정리
> **활용법**: AI가 생성한 코드를 "읽고, 판단하고, 수정"할 수 있는 최소한의 기초 체력을 기르는 것이 목적입니다.

---

## 0. 웹은 어떻게 동작하는가? (큰 그림)

## 간단한 웹 클라이언트 서버 구조
<img width="702" height="471" alt="image" src="https://github.com/user-attachments/assets/729d2f80-6120-4543-b18f-64de7f930793" />

## 웹 클라이언트 서버 구조와 웹 프로그램의 관계
<img width="1858" height="912" alt="image" src="https://github.com/user-attachments/assets/a00f78df-cd57-491f-8410-f17cbf387577" />

## 로드 밸런서 구조
<img width="1080" height="608" alt="image" src="https://github.com/user-attachments/assets/435f75c7-8fa1-4261-9485-fcceedf0289e" />

## 클라이언트-서버 응용 구조
<img width="100%"  alt="image" src="https://github.com/user-attachments/assets/af996c10-122b-4a12-96b2-e58c91fae08b" />


## 3-Tier 클라이언트-서버 구조
<img width="100%"  alt="image" src="https://github.com/user-attachments/assets/3a2366e7-c1ee-4b6b-a1c1-71dfc7fdad29" />

## Cloud 구조
<img width="1024" height="579" alt="image" src="https://github.com/user-attachments/assets/b854efc0-577f-483f-8f14-14f3eb3d7135" />



---

## 브라우저가 받은 3가지 파일의 역할 분담:

| 기술 | 역할 | 비유 |
|------|------|------|
| **HTML** | 구조 (뼈대) | 건물의 골조 |
| **CSS** | 디자인 (꾸미기) | 인테리어, 페인트 |
| **JavaScript** | 동작 (기능) | 전기, 엘리베이터 |

> 💡 **핵심 관점**: 세 기술은 역할이 분리되어 있습니다. "구조 따로, 스타일 따로, 동작 따로" — 이 **관심사의 분리(Separation of Concerns)** 개념이 웹개발 전체를 관통합니다.

---

# 1부. HTML — 웹 문서의 구조

## 1-1. HTML 기본 골격

모든 HTML 문서는 아래 구조로 시작합니다. 통째로 외우기보다 **각 부분의 역할**을 이해하세요.

```html
<!DOCTYPE html>              <!-- 이 문서가 HTML5 문서임을 선언 -->
<html lang="ko">             <!-- 문서의 시작, 언어는 한국어 -->
<head>
    <!-- head: 화면에 보이지 않는 문서 정보(메타데이터) -->
    <meta charset="UTF-8">   <!-- 한글 깨짐 방지 (필수!) -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- ↑ 모바일 화면 대응 (반응형의 시작점) -->
    <title>브라우저 탭에 표시될 제목</title>
</head>
<body>
    <!-- body: 실제 화면에 보이는 모든 내용 -->
    <h1>안녕하세요!</h1>
</body>
</html>
```

## 1-2. 반드시 알아야 할 핵심 태그

```html
<!-- 제목: h1(가장 큼) ~ h6(가장 작음). h1은 페이지당 1개가 원칙 -->
<h1>페이지 대제목</h1>
<h2>소제목</h2>

<!-- 문단 -->
<p>본문 내용은 p 태그 안에 작성합니다.</p>

<!-- 링크: href 속성에 이동할 주소 -->
<a href="https://www.google.com">구글로 이동</a>

<!-- 이미지: src(경로), alt(이미지 설명 - 접근성 필수) -->
<img src="cat.jpg" alt="고양이 사진">

<!-- 목록: ul(순서 없음), ol(순서 있음), li(항목) -->
<ul>
    <li>사과</li>
    <li>바나나</li>
</ul>

<!-- 영역 나누기: div(의미 없는 상자), span(문장 안의 일부분) -->
<div>블록 단위 영역</div>
<span>인라인 단위 영역</span>

<!-- 버튼과 입력창 -->
<button>클릭하세요</button>
<input type="text" placeholder="이름을 입력하세요">
```

## 1-3. 시맨틱 태그 — "의미 있는 구조"

`div`만 쓰지 말고, **의미를 담은 태그**로 페이지를 구성하는 습관을 들이세요.

```html
<body>
    <header>사이트 상단 (로고, 제목)</header>
    <nav>메뉴 (내비게이션)</nav>
    <main>
        <section>주제별 콘텐츠 묶음</section>
        <article>독립적인 글 (블로그 포스트 등)</article>
    </main>
    <footer>사이트 하단 (연락처, 저작권)</footer>
</body>
```

> 💡 **왜 중요한가?** 검색엔진(SEO)과 스크린리더가 페이지 구조를 이해할 수 있고, 협업 시 코드 가독성이 크게 좋아집니다. AI가 생성한 코드의 품질을 판단하는 기준이 되기도 합니다.

## 1-4. 폼(Form) — 사용자 입력 받기 (백엔드 연동의 출발점)

```html
<!-- action: 데이터를 보낼 서버 주소, method: 전송 방식 -->
<form action="/signup" method="POST">
    <label for="email">이메일</label>
    <input type="email" id="email" name="email" required>
    <!-- name 속성: 서버로 전송될 때의 "변수 이름" (매우 중요!) -->

    <label for="pw">비밀번호</label>
    <input type="password" id="pw" name="password" required>

    <button type="submit">가입하기</button>
</form>
```

> 💡 **풀스택 관점**: 폼의 `name` 속성 값이 서버(백엔드)에서 데이터를 받는 키(key)가 됩니다. 프론트와 백엔드가 만나는 첫 접점입니다.

---

# 2부. CSS — 웹 문서의 디자인

## 2-1. CSS 적용 방법과 기본 문법

```css
/* 문법: 선택자 { 속성: 값; } */
h1 {
    color: blue;        /* 글자색 */
    font-size: 24px;    /* 글자 크기 */
}
```

```html
<!-- 실무 표준: 별도의 CSS 파일을 만들어 연결 (head 안에 작성) -->
<link rel="stylesheet" href="style.css">
```

## 2-2. 선택자(Selector) — 누구를 꾸밀 것인가?

```css
/* 1) 태그 선택자: 모든 p 태그에 적용 */
p { color: gray; }

/* 2) 클래스 선택자(.): 재사용 가능. 가장 많이 사용! */
.highlight { background-color: yellow; }

/* 3) 아이디 선택자(#): 페이지에서 단 하나의 요소 */
#logo { width: 100px; }

/* 4) 자손 선택자: nav 안에 있는 a 태그만 */
nav a { text-decoration: none; }

/* 5) 상태 선택자: 마우스를 올렸을 때 */
button:hover { background-color: navy; }
```

```html
<p class="highlight">클래스가 적용된 문단</p>
<img id="logo" src="logo.png" alt="로고">
```

> 💡 **암기 팁**: `.클래스`는 여러 곳에 재사용, `#아이디`는 한 페이지에 하나. 실무에서는 클래스 위주로 작성합니다.

## 2-3. 박스 모델(Box Model) — CSS의 핵심 중의 핵심

모든 HTML 요소는 **네모 상자**입니다. 레이아웃이 어긋나는 문제의 90%는 박스 모델 이해 부족에서 나옵니다.

```
┌─────────────── margin (바깥 여백) ───────────────┐
│  ┌──────────── border (테두리) ────────────┐   │
│  │  ┌───────── padding (안쪽 여백) ─────┐  │   │
│  │  │                                    │  │   │
│  │  │         content (내용)             │  │   │
│  │  │                                    │  │   │
│  │  └────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────┘   │
└──────────────────────────────────────────────────┘
```

```css
.card {
    width: 300px;              /* 내용 영역의 너비 */
    padding: 20px;             /* 테두리 안쪽 여백 */
    border: 1px solid #ddd;    /* 테두리: 두께 스타일 색상 */
    margin: 10px;              /* 다른 요소와의 바깥 간격 */
    box-sizing: border-box;    /* ★ width에 padding, border 포함 (실무 필수 설정) */
}
```

> 💡 **실무 필수**: `* { box-sizing: border-box; }`를 CSS 최상단에 두는 것이 사실상 표준입니다. 이 설정이 없으면 `width: 300px + padding 20px = 실제 340px`이 되어 레이아웃이 틀어집니다.

## 2-4. Flexbox — 현대 레이아웃의 표준

요소를 가로/세로로 정렬하는 가장 중요한 도구입니다. **부모에게 `display: flex`를 주면 자식들이 정렬됩니다.**

```css
.container {
    display: flex;              /* 이 한 줄로 자식들이 가로로 배치됨 */
    justify-content: center;    /* 주축(가로) 정렬: center, space-between 등 */
    align-items: center;        /* 교차축(세로) 정렬 */
    gap: 16px;                  /* 자식들 사이의 간격 */
}
```

```html
<div class="container">
    <div>박스1</div>
    <div>박스2</div>
    <div>박스3</div>
</div>
<!-- 결과: 세 박스가 가운데 정렬되어 16px 간격으로 나란히 배치 -->
```

**가장 많이 쓰는 패턴 — 완전 중앙 정렬:**

```css
.center {
    display: flex;
    justify-content: center;  /* 가로 중앙 */
    align-items: center;      /* 세로 중앙 */
    height: 100vh;            /* 화면 전체 높이 */
}
```

## 2-5. 반응형 웹 — 미디어 쿼리

```css
/* 기본: PC 화면 스타일 */
.container { display: flex; }

/* 화면 너비가 768px 이하(모바일/태블릿)일 때 적용 */
@media (max-width: 768px) {
    .container {
        flex-direction: column;  /* 가로 배치 → 세로 배치로 전환 */
    }
}
```

> 💡 **핵심 개념만**: 반응형 = "화면 크기에 따라 다른 CSS를 적용하는 것". 세부 문법보다 이 개념과 `viewport` 메타 태그(1-1 참고)의 관계를 이해하는 것이 우선입니다.

---

# 3부. JavaScript — 웹 문서의 동작

## 3-1. 변수와 자료형

```javascript
// 변수 선언: const(재할당 불가, 기본값) vs let(재할당 가능)
const name = "홍길동";     // 문자열 (String)
let age = 25;              // 숫자 (Number)
const isStudent = true;    // 참/거짓 (Boolean)

age = 26;                  // let은 값 변경 가능 ✅
// name = "김철수";        // const는 값 변경 불가 ❌ 에러 발생!

// var는 옛날 방식이므로 사용하지 않습니다.
```

```javascript
// 배열: 여러 값을 순서대로 담는 목록
const fruits = ["사과", "바나나", "포도"];
console.log(fruits[0]);        // "사과" (0번부터 시작!)

// 객체: {키: 값} 쌍으로 데이터를 묶음 — 백엔드와 주고받는 데이터의 기본 형태
const user = {
    name: "홍길동",
    age: 25
};
console.log(user.name);        // "홍길동"
```

> 💡 **풀스택 관점**: 객체(Object)는 서버와 주고받는 **JSON 데이터**와 모양이 같습니다. 객체를 다루는 능력 = API 데이터를 다루는 능력입니다.

## 3-2. 조건문과 반복문

```javascript
// 조건문: 상황에 따라 다르게 동작
const score = 85;

if (score >= 90) {
    console.log("A등급");
} else if (score >= 80) {
    console.log("B등급");      // 85점이므로 이것이 실행됨
} else {
    console.log("재시험");
}
```

```javascript
// 반복문: 배열을 순회하는 현대적 방법
const fruits = ["사과", "바나나", "포도"];

for (const fruit of fruits) {
    console.log(fruit);        // 사과, 바나나, 포도 차례로 출력
}
```

## 3-3. 함수 — 코드를 묶어 재사용하기

```javascript
// 1) 함수 선언문
function add(a, b) {
    return a + b;              // 결과를 돌려줌
}
console.log(add(3, 5));        // 8

// 2) 화살표 함수 (현대 JS에서 매우 많이 사용 — 반드시 읽을 줄 알아야 함)
const multiply = (a, b) => a * b;
console.log(multiply(3, 5));   // 15
```

> 💡 화살표 함수는 React 등 최신 프레임워크 코드에서 끊임없이 등장합니다. "함수를 짧게 쓰는 문법"으로 이해하면 됩니다.

## 3-4. DOM 조작 — JS로 HTML을 바꾸기

**DOM(Document Object Model)**: 브라우저가 HTML을 JS로 다룰 수 있게 만든 객체 구조입니다.

```html
<h1 id="title">원래 제목</h1>
<button id="btn">클릭</button>
```

```javascript
// 1) 요소 선택하기 (CSS 선택자를 그대로 사용)
const title = document.querySelector("#title");
const btn = document.querySelector("#btn");

// 2) 내용 바꾸기
title.textContent = "바뀐 제목!";

// 3) 스타일 바꾸기
title.style.color = "red";

// 4) 클래스 추가/제거 (CSS와 연동하는 실무 패턴)
title.classList.add("active");
```

## 3-5. 이벤트 — 사용자의 행동에 반응하기

```javascript
const btn = document.querySelector("#btn");

// "버튼이 클릭되면(click), 이 함수를 실행하라"
btn.addEventListener("click", () => {
    alert("버튼이 클릭되었습니다!");
});
```

**미니 실습 예제 — 클릭 카운터 (핵심 개념 총집합):**

```html
<p id="count">0</p>
<button id="plus">+1</button>

<script>
    let count = 0;                                    // 상태(데이터)
    const display = document.querySelector("#count"); // 요소 선택

    document.querySelector("#plus").addEventListener("click", () => {
        count = count + 1;                // 1. 데이터를 바꾸고
        display.textContent = count;      // 2. 화면에 반영한다
    });
</script>
```

> 💡 **"데이터가 바뀌면 → 화면을 갱신한다"** — 이 흐름이 나중에 배울 React 같은 프레임워크의 핵심 사상입니다. 이 예제를 완벽히 이해하면 프레임워크 학습이 훨씬 수월해집니다.

## 3-6. 비동기와 fetch — 서버에서 데이터 가져오기 (풀스택의 연결고리)

```javascript
// async/await: "서버 응답을 기다렸다가(await) 다음 줄을 실행"
async function getUsers() {
    try {
        // 1. 서버(API)에 데이터 요청
        const response = await fetch("https://jsonplaceholder.typicode.com/users");

        // 2. 응답을 JSON(자바스크립트 객체)으로 변환
        const users = await response.json();

        // 3. 데이터 사용
        console.log(users[0].name);   // 첫 번째 사용자의 이름 출력
    } catch (error) {
        console.error("요청 실패:", error);   // 네트워크 오류 등 처리
    }
}

getUsers();
```

> 💡 **풀스택 관점**: 이것이 프론트엔드와 백엔드가 대화하는 방식입니다.
> `프론트(fetch 요청) → 백엔드(API가 JSON 응답) → 프론트(화면에 표시)`
> 앞으로 배울 백엔드 과정은 이 `fetch`가 호출하는 **서버 쪽 API를 직접 만드는 것**입니다.

---

# 4부. 셋을 하나로 — 종합 미니 예제

아래는 HTML(구조) + CSS(디자인) + JS(동작)가 협력하는 최소 단위의 완성 예제입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>할 일 목록</title>
    <style>
        * { box-sizing: border-box; }              /* 실무 기본 설정 */
        body {
            display: flex;
            justify-content: center;                /* 가로 중앙 정렬 */
            font-family: sans-serif;
        }
        .todo-app { width: 300px; }
        input { width: 70%; padding: 8px; }
        button { padding: 8px 12px; cursor: pointer; }
        li { margin: 8px 0; }
    </style>
</head>
<body>
    <div class="todo-app">
        <h1>할 일 목록</h1>
        <input id="todo-input" type="text" placeholder="할 일 입력">
        <button id="add-btn">추가</button>
        <ul id="todo-list"></ul>   <!-- JS가 여기에 항목을 추가함 -->
    </div>

    <script>
        const input = document.querySelector("#todo-input");
        const list = document.querySelector("#todo-list");

        document.querySelector("#add-btn").addEventListener("click", () => {
            if (input.value === "") return;   // 빈 입력 방지 (유효성 검사)

            const li = document.createElement("li");  // 새 li 요소 생성
            li.textContent = input.value;             // 입력값을 내용으로
            list.appendChild(li);                     // 목록에 추가
            input.value = "";                         // 입력창 비우기
        });
    </script>
</body>
</html>
```

---

# 5부. AI 시대의 학습 가이드

## 왜 AI가 코드를 짜주는데도 이걸 배워야 하는가?

| AI가 해주는 것 | 사람이 해야 하는 것 |
|----------------|---------------------|
| 코드 생성 | 생성된 코드가 **맞는지 판단** |
| 문법 암기 대체 | 구조와 개념의 **이해** |
| 반복 작업 자동화 | 요구사항을 **정확히 설명(프롬프트)** |
| 에러 메시지 해석 | 어디를 봐야 할지 **감을 잡는 것** |

- **읽기 > 쓰기**: 처음에는 코드를 "잘 쓰는 것"보다 "잘 읽는 것"이 목표입니다. AI 코드 리뷰가 곧 실무 역량입니다.
- **개념 어휘력**: "박스 모델", "이벤트 리스너", "비동기"라는 용어를 알아야 AI에게 정확히 질문할 수 있습니다.
- **디버깅 습관**: `console.log()`와 브라우저 개발자 도구(F12)를 항상 켜두는 습관을 들이세요.

## 학습 우선순위 요약 (비전공자 기준)

```
1순위: HTML 구조 + 폼 / CSS 박스모델 + Flexbox / JS 변수·함수·DOM·이벤트
2순위: 시맨틱 태그, 반응형 개념, 배열·객체 다루기, fetch와 비동기
3순위: 세부 속성·문법 암기 (→ 이건 AI와 검색에 맡겨도 됩니다)
```

> **한 줄 정리**: 구조(HTML) → 디자인(CSS) → 동작(JS) → 서버 연결(fetch)의 큰 흐름을 몸에 익히면, 나머지는 AI와 함께 채워나갈 수 있습니다.
