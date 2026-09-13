HTML → CSS → SCSS(Sass) → Bootstrap 순서로 학습하는 것은 매우 자연스럽습니다. 특히 비전공자에게는 **“직접 CSS로 만들어 본 뒤, Bootstrap이 그 작업을 얼마나 줄여주는지 체감하게 하는 방식”**이 좋습니다.

중요한 점은 Bootstrap을 별개의 기술로 보기보다, **HTML + CSS + 일부 JavaScript 작업을 미리 만들어 둔 CSS/JS 프레임워크**라고 이해시키는 것입니다.

## 1. 전체 학습 흐름

```text
HTML
  ↓
웹 문서의 구조 만들기

CSS
  ↓
디자인 / 배치 / 반응형

SCSS(Sass)
  ↓
CSS를 더 편하게 작성하고 관리

Bootstrap
  ↓
자주 사용하는 CSS/UI를 미리 만들어 둔 프레임워크
```

학생들에게는 다음처럼 설명하면 가장 직관적입니다.

> HTML은 건물의 구조,
> CSS는 인테리어,
> SCSS는 인테리어 설계를 효율적으로 관리하는 도구,
> Bootstrap은 미리 만들어 놓은 인테리어 부품 세트입니다.

---

# 2. HTML에서 반드시 알아야 할 내용

Bootstrap을 배우기 전에 HTML을 완벽하게 알 필요는 없습니다. 하지만 다음 정도는 반드시 알아야 합니다.

### 기본 문서 구조

```html
<!DOCTYPE html>
<html>
<head>
    <title>쇼핑몰</title>
</head>

<body>

    <h1>상품 목록</h1>

</body>
</html>
```

특히 다음 구조를 이해해야 합니다.

```text
html
 ├─ head
 │   ├─ meta
 │   ├─ title
 │   └─ link
 │
 └─ body
```

Bootstrap에서 CSS 파일을 연결하기 때문에 `<link>`의 의미도 알아야 합니다.

---

## 자주 사용하는 HTML 태그

최소한 다음 태그는 익숙해야 합니다.

```html
<h1>제목</h1>

<p>문장</p>

<a href="#">링크</a>

<img src="product.jpg">

<div>영역</div>

<span>텍스트 영역</span>

<button>버튼</button>
```

특히 Bootstrap에서는 **div를 매우 많이 사용합니다.**

예:

```html
<div class="container">
    <div class="row">
        <div class="col">
            상품
        </div>
    </div>
</div>
```

따라서 `<div>`와 `class`를 반드시 이해해야 합니다.

---

# 3. class와 id

Bootstrap을 배우기 전에 가장 중요한 HTML 개념 중 하나입니다.

```html
<div class="product">
    상품
</div>
```

CSS:

```css
.product {
    color: blue;
}
```

즉,

```text
HTML

class="product"

        ↓

CSS

.product
```

Bootstrap도 동일합니다.

```html
<button class="btn btn-primary">
    구매하기
</button>
```

여기서

```text
btn
btn-primary
```

는 Bootstrap에서 미리 만들어 놓은 CSS 클래스입니다.

Bootstrap을 이해하는 핵심이 바로 이것입니다.

> **Bootstrap = 미리 만들어진 class를 가져다가 사용하는 것**

---

# 4. CSS에서 반드시 알아야 할 내용

Bootstrap을 배우기 전에 CSS에서 가장 중요한 것은 크게 6가지입니다.

```text
① 선택자
② 박스 모델
③ display
④ Flex
⑤ Grid
⑥ 반응형
```

이 정도를 이해하면 Bootstrap 학습이 훨씬 쉬워집니다.

---

# 5. CSS 선택자

```html
<p class="title">상품 목록</p>
```

```css
.title {
    color: blue;
}
```

최소한 다음 정도는 알아야 합니다.

```css
p {
}

.title {
}

#header {
}
```

의미:

```text
p       태그 선택자
.title  class 선택자
#header id 선택자
```

Bootstrap에서는 거의 대부분 class를 사용합니다.

---

# 6. CSS 박스 모델

Bootstrap을 배우기 전에 반드시 이해시키는 것이 좋습니다.

```text
┌─────────────────────┐
│       margin        │
│  ┌───────────────┐  │
│  │    border     │  │
│  │ ┌───────────┐ │  │
│  │ │ padding   │ │  │
│  │ │ ┌───────┐ │ │  │
│  │ │ │content│ │ │  │
│  │ │ └───────┘ │ │  │
│  │ └───────────┘ │  │
│  └───────────────┘  │
└─────────────────────┘
```

CSS:

```css
.box {
    width: 300px;

    padding: 20px;

    border: 1px solid black;

    margin: 20px;
}
```

Bootstrap에서는 이것을 다음처럼 간단히 표현합니다.

```html
<div class="p-3 m-3 border">
```

즉,

```text
p-3 → padding
m-3 → margin
border → border
```

따라서 CSS 박스 모델을 모르면 Bootstrap 클래스가 단순 암기 과목이 됩니다.

---

# 7. display

최소한 다음 정도는 알아야 합니다.

```css
display: block;

display: inline;

display: flex;

display: grid;

display: none;
```

Bootstrap에서도 그대로 등장합니다.

```html
<div class="d-flex">
```

의미는 사실상

```css
display: flex;
```

입니다.

---

# 8. Flex는 반드시 학습하는 것이 좋다

Bootstrap에서 상당히 많이 사용됩니다.

CSS:

```css
.container {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

Bootstrap:

```html
<div class="d-flex justify-content-center align-items-center">
```

둘을 비교해서 가르치면 Bootstrap을 매우 쉽게 이해합니다.

```text
CSS

display: flex
justify-content: center
align-items: center

        ↓

Bootstrap

d-flex
justify-content-center
align-items-center
```

---

# 9. Grid도 기본 개념은 알아야 한다

CSS Grid:

```css
.container {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
}
```

Bootstrap의 Grid는 방식이 조금 다릅니다.

```html
<div class="container">

    <div class="row">

        <div class="col">
            상품1
        </div>

        <div class="col">
            상품2
        </div>

        <div class="col">
            상품3
        </div>

    </div>

</div>
```

Bootstrap에서 매우 중요한 개념입니다.

```text
container
    ↓
row
    ↓
col
```

이 세 가지는 반드시 익혀야 합니다.

---

# 10. Bootstrap의 12 Column 시스템

Bootstrap Grid의 핵심입니다.

한 줄을 **12칸**으로 생각합니다.

```text
|----------------------------|
| 1 2 3 4 5 6 7 8 9 10 11 12 |
|----------------------------|
```

예를 들어 3등분:

```html
<div class="row">

    <div class="col-4">상품1</div>

    <div class="col-4">상품2</div>

    <div class="col-4">상품3</div>

</div>
```

```text
4 + 4 + 4 = 12
```

2등분:

```html
<div class="row">

    <div class="col-6">왼쪽</div>

    <div class="col-6">오른쪽</div>

</div>
```

```text
6 + 6 = 12
```

이것은 Bootstrap에서 가장 중요한 내용 중 하나입니다.

---

# 11. 반응형 CSS

Bootstrap 전에 반드시 개념은 이해해야 합니다.

CSS에서는 보통 미디어 쿼리를 사용합니다.

```css
.product {
    width: 25%;
}

@media (max-width: 768px) {

    .product {
        width: 100%;
    }

}
```

Bootstrap에서는 이것을 훨씬 편리하게 처리합니다.

```html
<div class="col-12 col-md-6 col-lg-3">
```

의미:

```text
모바일
col-12
→ 한 줄에 1개

태블릿
col-md-6
→ 한 줄에 2개

데스크탑
col-lg-3
→ 한 줄에 4개
```

따라서 먼저 학생들에게 다음 개념을 알려주는 것이 좋습니다.

```text
Mobile
Tablet
Desktop
```

그리고

```text
작은 화면
   ↓
중간 화면
   ↓
큰 화면
```

에 따라 레이아웃이 바뀐다는 개념을 이해시키면 됩니다.

---

# 12. SCSS는 어느 정도까지 배워야 하는가

Bootstrap 전에 SCSS를 너무 깊게 배울 필요는 없습니다.

비전공자 기준으로는 다음 4개 정도면 충분합니다.

```text
① 변수
② 중첩
③ 함수/믹스인
④ 파일 분리
```

---

## 변수

CSS:

```css
button {
    background: blue;
}

h1 {
    color: blue;
}
```

SCSS:

```scss
$main-color: blue;

button {
    background: $main-color;
}

h1 {
    color: $main-color;
}
```

---

# 13. 중첩

CSS:

```css
nav ul {
    list-style: none;
}

nav ul li {
    display: inline;
}
```

SCSS:

```scss
nav {

    ul {

        list-style: none;

        li {
            display: inline;
        }
    }
}
```

---

# 14. SCSS에서 꼭 설명해야 하는 점

학생들이 가장 많이 혼동하는 부분입니다.

브라우저는 SCSS를 직접 읽지 못합니다.

```text
SCSS
 ↓
Sass Compiler
 ↓
CSS
 ↓
Browser
```

즉,

```scss
$main-color: blue;
```

를 브라우저가 직접 실행하는 것이 아닙니다.

컴파일하면:

```css
button {
    background-color: blue;
}
```

가 됩니다.

---

# 15. 그러면 Bootstrap은 무엇인가?

여기에서 Bootstrap을 소개하면 자연스럽습니다.

CSS로 버튼을 만들면:

```css
button {
    background-color: blue;
    color: white;

    padding: 10px 20px;

    border: none;

    border-radius: 5px;
}
```

하지만 Bootstrap은:

```html
<button class="btn btn-primary">
    구매하기
</button>
```

이면 됩니다.

즉,

```text
직접 CSS 작성

        ↓

Bootstrap

미리 만들어 놓은 CSS 사용
```

입니다.

---

# 16. Bootstrap에서 반드시 배워야 할 내용

비전공자 과정이라면 Bootstrap 전체를 가르칠 필요는 없습니다.

다음 **8개 영역**이면 충분합니다.

| 영역           | 반드시 알아야 할 내용          |
| ------------ | --------------------- |
| Bootstrap 연결 | CDN                   |
| Layout       | container             |
| Grid         | row, col              |
| 반응형          | sm, md, lg, xl        |
| Utility      | margin, padding       |
| Flex         | d-flex                |
| Component    | Button, Card, Navbar  |
| Form         | input, select, button |

---

# 17. Bootstrap CDN

가장 먼저 보여주는 것이 좋습니다.

개념은 간단합니다.

```text
내가 Bootstrap CSS를 직접 만들지 않고

인터넷에서 Bootstrap CSS 파일을 가져온다.
```

HTML에서는 Bootstrap CSS와 JavaScript를 연결한 후 Bootstrap class를 사용하게 됩니다.

학생들에게는 CDN 문법 자체보다 다음 구조를 이해시키는 것이 중요합니다.

```text
HTML
 +
Bootstrap CSS
 +
Bootstrap JS
```

---

# 18. 가장 중요한 Bootstrap Utility

이 부분을 반드시 학습시키는 것을 권합니다.

### 여백

```html
<div class="m-3">
```

```text
m → margin
```

```html
<div class="p-3">
```

```text
p → padding
```

방향:

```text
mt → margin-top
mb → margin-bottom
ms → margin-start
me → margin-end

pt
pb
ps
pe
```

예:

```html
<h1 class="mt-5 mb-3">
    상품 목록
</h1>
```

---

# 19. Bootstrap 색상

다음 정도는 외울 필요 없이 익숙해지면 됩니다.

```text
primary
secondary
success
danger
warning
info
light
dark
```

예:

```html
<button class="btn btn-primary">
    저장
</button>

<button class="btn btn-danger">
    삭제
</button>

<button class="btn btn-success">
    완료
</button>
```

---

# 20. Button

Bootstrap 입문에서 가장 좋은 예제입니다.

```html
<button class="btn btn-primary">저장</button>

<button class="btn btn-danger">삭제</button>

<button class="btn btn-success">확인</button>
```

학생들이 바로 결과를 확인할 수 있습니다.

---

# 21. Card

쇼핑몰 프로젝트라면 특히 중요합니다.

```html
<div class="card">

    <img src="product.jpg"
         class="card-img-top">

    <div class="card-body">

        <h5 class="card-title">
            노트북
        </h5>

        <p class="card-text">
            1,200,000원
        </p>

        <button class="btn btn-primary">
            구매
        </button>

    </div>

</div>
```

다음 프로젝트에서 바로 사용할 수 있습니다.

```text
상품
공지사항
게시글
프로필
대시보드
```

---

# 22. Form

웹 서비스 개발에서는 반드시 필요합니다.

```html
<div class="mb-3">

    <label class="form-label">
        이메일
    </label>

    <input type="email"
           class="form-control">

</div>
```

학생들에게 다음 대응 관계를 알려주면 좋습니다.

```text
일반 HTML

<input>

        ↓

Bootstrap

<input class="form-control">
```

---

# 23. Navbar

실제 웹사이트 구조를 만들 때 매우 유용합니다.

```text
쇼핑몰

상품
장바구니
주문내역
로그인
```

Bootstrap의 Navbar를 사용하면 복잡한 메뉴를 빠르게 만들 수 있습니다.

다만 처음부터 Navbar의 긴 예제를 암기시키기보다는 Bootstrap 공식 예제를 가져와서 **구조를 읽고 수정할 수 있는 능력**을 기르는 것이 더 중요합니다.

---

# 24. Bootstrap에서 암기하지 않아도 되는 것

이 부분은 교육에서 상당히 중요합니다.

학생들에게 Bootstrap 클래스를 전부 외우게 할 필요가 없습니다.

예를 들어:

```text
btn
card
navbar
modal
accordion
dropdown
badge
alert
carousel
```

를 모두 암기시키는 방식은 효율적이지 않습니다.

오히려 다음 능력이 중요합니다.

```text
필요한 UI 판단
       ↓
Bootstrap 문서 검색
       ↓
예제 코드 가져오기
       ↓
내 웹페이지에 적용
       ↓
필요한 부분 수정
```

AX 시대에는 이 능력이 더욱 중요합니다.

---

# 25. JavaScript도 아주 조금 필요하다

Bootstrap을 학습하면서 다음과 같은 UI를 만나게 됩니다.

```text
Dropdown
Modal
Collapse
Navbar
Carousel
Accordion
```

이들은 동작이 있기 때문에 JavaScript와 관련됩니다.

다만 Bootstrap 입문 전에 깊은 JS를 알 필요는 없습니다.

최소한:

```javascript
const button = document.querySelector("#btn");

button.addEventListener("click", function() {

    alert("버튼 클릭");

});
```

정도로

```text
요소 선택
이벤트
버튼 클릭
```

개념 정도는 알고 있으면 충분합니다.

---

# 26. 실제 교육에서는 이 순서를 추천합니다

비전공자 수업이라면 다음 흐름이 가장 자연스럽습니다.

```text
1단계
HTML

문서 구조
태그
div
form
class
id

        ↓

2단계
CSS

선택자
색상
폰트
Box Model
display

        ↓

3단계
Layout

Flex
Grid

        ↓

4단계
반응형

viewport
media query

        ↓

5단계
SCSS

변수
중첩
mixin
컴파일

        ↓

6단계
Bootstrap

container
row
col
utility

        ↓

7단계
Bootstrap Component

button
card
navbar
form
modal
```

---

# 27. Bootstrap 수업의 핵심은 CSS와 비교하는 것

강의에서는 아래와 같은 비교 방식이 매우 효과적입니다.

### CSS

```css
.box {
    display: flex;

    justify-content: center;

    margin-top: 20px;

    padding: 20px;
}
```

### Bootstrap

```html
<div class="
    d-flex
    justify-content-center
    mt-3
    p-3
">
```

그리고 다음처럼 설명하면 됩니다.

```text
CSS 작성

display:flex
        ↓
d-flex


justify-content:center
        ↓
justify-content-center


margin-top
        ↓
mt


padding
        ↓
p
```

이렇게 배우면 Bootstrap이 새로운 문법처럼 느껴지지 않습니다.

---

# 28. 비전공자 기준으로 반드시 기억해야 할 핵심 10개

Bootstrap 학습 직전까지 학생이 아래 10가지만 알고 있다면 충분하다고 봅니다.

1. **HTML은 구조, CSS는 디자인이다.**
2. `<div>`로 영역을 나눌 수 있다.
3. `class`로 CSS 스타일을 연결한다.
4. CSS 선택자의 `.class` 의미를 안다.
5. `margin`과 `padding` 차이를 안다.
6. `display:flex`의 기본 개념을 안다.
7. Grid가 행과 열을 배치한다는 것을 안다.
8. 반응형 웹의 의미를 안다.
9. SCSS는 CSS를 편하게 작성하는 도구이며 CSS로 컴파일된다는 것을 안다.
10. Bootstrap은 **미리 만들어진 CSS/JS 클래스와 컴포넌트를 사용하는 프레임워크**라는 것을 안다.

그리고 Bootstrap에 들어가면 우선 이것만 집중하면 됩니다.

```text
container
row
col

btn

card

form-control

m / p

d-flex

반응형
col-sm
col-md
col-lg
```

이 정도만 제대로 사용할 수 있어도 **간단한 쇼핑몰, 관리자 페이지, 게시판, 로그인 화면, 대시보드 UI**를 충분히 만들 수 있습니다.

특히 현재처럼 최종적으로 **React/FastAPI 기반 AX 서비스 개발**까지 이어지는 과정이라면, Bootstrap 수업의 목표를 “Bootstrap을 많이 아는 것”이 아니라 **HTML/CSS를 직접 작성하는 단계에서 컴포넌트 기반 UI 개발로 넘어가는 중간 단계**로 잡는 것이 가장 적절합니다. React에서 Bootstrap, Tailwind, MUI 같은 UI 체계를 만날 때도 이 개념이 그대로 연결됩니다.
