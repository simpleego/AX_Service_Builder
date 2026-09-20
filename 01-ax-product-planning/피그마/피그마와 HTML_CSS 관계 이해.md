# 피그마와 HTML/CSS 관계 이해
---


- 피그마(Figma)와 HTML/CSS의 관계는 크게 보면 이렇게 이해하면 가장 쉽습니다.
- **Figma는 “화면을 어떻게 보이게 할 것인가”를 시각적으로 설계하는 도구이고, HTML/CSS는 그 설계를 실제 웹페이지로 구현하는 기술**입니다.
- 특히 Figma의 요소 중 상당수는 HTML보다는 **CSS와 더 직접적인 관계**를 갖습니다.

### 1. 전체적인 대응 관계

| Figma 요소/기능        | HTML에서 대응                     | CSS에서 대응                                           |
| ------------------ | ----------------------------- | -------------------------------------------------- |
| Frame              | `div`, `section`, `main` 등    | `width`, `height`, `display`, `position`           |
| Group              | `div`                         | 요소 묶음, 레이아웃                                        |
| Text               | `h1`, `p`, `span`, `button` 등 | `font-size`, `font-weight`, `color`, `line-height` |
| Rectangle          | `div`                         | `width`, `height`, `background`, `border`          |
| Image              | `img`                         | `width`, `height`, `object-fit`                    |
| Auto Layout        | 여러 HTML 요소                    | `display:flex`가 가장 유사                              |
| Grid               | 여러 HTML 요소                    | `display:grid`                                     |
| Padding            | -                             | `padding`                                          |
| Gap / Spacing      | -                             | `gap`                                              |
| Margin 개념          | -                             | `margin`                                           |
| Fill               | -                             | `background-color`                                 |
| Stroke             | -                             | `border`                                           |
| Corner Radius      | -                             | `border-radius`                                    |
| Shadow             | -                             | `box-shadow`                                       |
| Opacity            | -                             | `opacity`                                          |
| Alignment          | -                             | `justify-content`, `align-items`                   |
| Constraints        | -                             | 반응형 CSS, `%`, `flex`, `grid`, `position`           |
| Component          | 재사용 HTML 구조                   | 재사용 CSS / React Component 등                        |
| Variant            | 상태별 HTML 구조                   | 클래스, `:hover`, `:active` 등                         |
| Prototype          | `<a>`, `<button>` 등           | CSS보다는 JavaScript와 관계                              |
| Component Instance | 동일 구조 반복                      | 같은 CSS 클래스 재사용                                     |

핵심적으로는 다음처럼 보면 됩니다.

> **Figma의 Frame/Component → HTML의 구조**
> **Figma의 색상·크기·정렬·간격 → CSS의 스타일**
> **Figma의 클릭·페이지 이동 → JavaScript 또는 링크**

---

# 2. 가장 중요한 Figma의 Frame

Figma에서 가장 많이 사용하는 것이 **Frame**입니다.

예를 들어 Figma에서 다음처럼 화면을 설계했다고 하겠습니다.

```text
Frame
 ├─ Logo
 ├─ Menu
 └─ Login Button
```

웹에서는 대략 다음과 같이 구현할 수 있습니다.

```html
<header>
    <img src="logo.png" alt="logo">

    <nav>
        <a href="#">홈</a>
        <a href="#">상품</a>
        <a href="#">고객센터</a>
    </nav>

    <button>로그인</button>
</header>
```

즉 Figma의 Frame이 반드시 HTML의 특정 태그 하나와 대응되는 것은 아닙니다.

디자인의 의미에 따라

```html
<div>
<section>
<header>
main>
article>
footer>
nav>
```

등으로 변환됩니다.

그래서 학생들에게는

> **Figma Frame ≈ HTML의 컨테이너**

라고 설명하면 이해하기 쉽습니다.

---

# 3. Figma Auto Layout과 CSS Flex

Figma를 HTML/CSS와 연결해서 학습할 때 **가장 중요한 개념 중 하나**입니다.

Figma의 Auto Layout은 CSS의

```css
display: flex;
```

와 상당히 유사합니다.

예를 들어 Figma에서

```text
Auto Layout
Direction : Horizontal

[메뉴1] [메뉴2] [메뉴3]
```

를 만들었다면 CSS에서는

```html
<nav class="menu">
    <a>메뉴1</a>
    <a>메뉴2</a>
    <a>메뉴3</a>
</nav>
```

```css
.menu {
    display: flex;
    gap: 20px;
}
```

처럼 구현합니다.

따라서 다음 관계를 기억하면 좋습니다.

| Figma Auto Layout | CSS Flex                         |
| ----------------- | -------------------------------- |
| Horizontal        | `flex-direction: row`            |
| Vertical          | `flex-direction: column`         |
| Gap               | `gap`                            |
| Padding           | `padding`                        |
| Align Left        | `justify-content: flex-start`    |
| Align Center      | `justify-content: center`        |
| Space Between     | `justify-content: space-between` |
| Vertical Center   | `align-items: center`            |

예를 들어 Figma에서

```text
Auto Layout

Direction      Horizontal
Gap            20
Padding        10
Alignment      Center
```

이면 CSS에서는 대략

```css
.container {
    display: flex;
    gap: 20px;
    padding: 10px;
    align-items: center;
}
```

가 됩니다.

---

# 4. Figma의 Fill과 CSS background

Figma에서 객체를 선택하면 흔히

```text
Fill
```

이라는 항목이 나옵니다.

예를 들어

```text
Fill
#3366FF
```

이면 CSS에서는

```css
background-color: #3366ff;
```

입니다.

텍스트의 Fill이라면 보통

```css
color: #3366ff;
```

가 됩니다.

즉 같은 Fill이라도 대상에 따라 다릅니다.

```text
Figma Rectangle Fill
        ↓
CSS background-color

Figma Text Fill
        ↓
CSS color
```

---

# 5. Stroke와 border

Figma의

```text
Stroke
```

는 CSS의

```css
border
```

와 거의 대응합니다.

예를 들어 Figma가

```text
Stroke
1px
#CCCCCC
```

이면

```css
border: 1px solid #cccccc;
```

로 구현할 수 있습니다.

---

# 6. Corner Radius와 border-radius

Figma에서 카드나 버튼 모서리를 둥글게 만드는

```text
Corner Radius
```

는 CSS의

```css
border-radius
```

와 대응합니다.

예를 들어

```text
Radius : 10
```

이면

```css
border-radius: 10px;
```

입니다.

버튼 디자인:

```text
┌──────────────────┐
│      로그인       │
└──────────────────┘
```

CSS:

```css
button {
    border-radius: 10px;
}
```

---

# 7. Drop Shadow와 box-shadow

Figma의 Effect 중

```text
Drop Shadow
```

는 CSS의

```css
box-shadow
```

입니다.

Figma에서

```text
X       0
Y       4
Blur    10
Opacity 20%
```

정도로 지정했다면 CSS에서는 대략

```css
box-shadow: 0 4px 10px rgba(0,0,0,0.2);
```

처럼 표현합니다.

---

# 8. Figma Text와 HTML/CSS

Figma의 Text는 HTML에서는 의미에 따라 태그가 달라집니다.

예를 들어 Figma에서 모두 그냥 Text 객체이지만 웹에서는 다음처럼 달라집니다.

```text
쇼핑몰              → h1
오늘의 추천 상품     → h2
상품 설명            → p
가격                 → span
로그인               → button
메뉴                 → a
```

HTML:

```html
<h1>쇼핑몰</h1>

<h2>오늘의 추천 상품</h2>

<p>편안한 운동화입니다.</p>

<span>59,000원</span>

<button>구매하기</button>
```

글자 스타일은 CSS가 담당합니다.

```css
h1 {
    font-size: 32px;
    font-weight: 700;
    color: #222;
}
```

Figma 속성과 연결하면

| Figma Text 속성  | CSS              |
| -------------- | ---------------- |
| Font           | `font-family`    |
| Size           | `font-size`      |
| Weight         | `font-weight`    |
| Line height    | `line-height`    |
| Letter spacing | `letter-spacing` |
| Alignment      | `text-align`     |
| Fill           | `color`          |

---

# 9. Figma 이미지와 HTML img

Figma에서 사진을 배치했다면 웹에서는 보통

```html
<img src="product.jpg" alt="상품 이미지">
```

입니다.

Figma에서 이미지 크기를

```text
300 × 200
```

으로 했다면

```css
img {
    width: 300px;
    height: 200px;
}
```

처럼 할 수 있습니다.

사진 비율 때문에 자주 사용하는 CSS가

```css
object-fit: cover;
```

입니다.

```css
.product-image {
    width: 300px;
    height: 200px;
    object-fit: cover;
}
```

Figma에서 이미지 Frame을 잘라 보여주는 것과 비슷합니다.

---

# 10. Figma Width / Height

Figma에서

```text
W : 300
H : 200
```

이면 CSS에서는 기본적으로

```css
width: 300px;
height: 200px;
```

입니다.

하지만 실제 반응형 웹에서는 고정 크기보다

```css
width: 100%;
max-width: 1200px;
```

같이 사용하는 경우가 많습니다.

따라서

```text
Figma
Width = 1200px
```

라고 되어 있다고 해서 반드시

```css
width: 1200px;
```

으로 작성해야 하는 것은 아닙니다.

오히려

```css
.container {
    width: 90%;
    max-width: 1200px;
}
```

처럼 작성하는 것이 더 적절할 수 있습니다.

---

# 11. Hug / Fill / Fixed와 CSS

최근 Figma를 배우는 학생들이 가장 헷갈리는 부분입니다.

Auto Layout에서 크기를 설정할 때

```text
Fixed
Hug contents
Fill container
```

를 사용합니다.

CSS와 비교하면 대략 다음과 같습니다.

| Figma          | CSS 개념                        |
| -------------- | ----------------------------- |
| Fixed          | `width: 200px`                |
| Hug contents   | `width: fit-content` 또는 내용 크기 |
| Fill container | `width:100%` 또는 `flex:1`      |

예를 들어

```text
버튼

Hug contents
```

이면 글자 길이에 따라 버튼 크기가 변합니다.

CSS:

```css
button {
    width: fit-content;
    padding: 10px 20px;
}
```

반대로

```text
Fill container
```

이면

```css
button {
    width: 100%;
}
```

또는 Flex 환경에서는

```css
button {
    flex: 1;
}
```

과 비슷합니다.

---

# 12. Figma Constraints와 반응형 CSS

Figma에서

```text
Constraints

Left
Right
Center
Scale
```

등을 설정할 수 있습니다.

이것은 웹에서는 주로

```text
Flex
Grid
%
max-width
min-width
position
media query
```

등으로 구현합니다.

예를 들어 데스크톱 디자인이

```text
┌────────────────────────────────────┐
│ Logo        Menu          Login    │
└────────────────────────────────────┘
```

이고 모바일에서는

```text
┌─────────────────┐
│ Logo      ☰     │
└─────────────────┘
```

로 변한다면 CSS에서는

```css
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

@media (max-width: 768px) {

    .menu {
        display: none;
    }

}
```

같은 반응형 처리가 필요합니다.

즉

> Figma Constraints = CSS 한 가지 속성

이라고 생각하면 안 되고,

> **Figma Constraints는 웹의 반응형 레이아웃 개념과 대응한다**

고 이해하는 것이 정확합니다.

---

# 13. Figma Grid와 CSS Grid

Figma에서는 레이아웃을 맞추기 위해 Layout Grid를 사용할 수 있습니다.

예를 들어 상품을

```text
상품1 상품2 상품3

상품4 상품5 상품6
```

처럼 배치한다면 CSS Grid가 매우 적합합니다.

```html
<div class="products">

    <div>상품1</div>
    <div>상품2</div>
    <div>상품3</div>

    <div>상품4</div>
    <div>상품5</div>
    <div>상품6</div>

</div>
```

```css
.products {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
}
```

따라서 실무적으로는 다음처럼 이해하면 좋습니다.

```text
Figma Auto Layout
        ↓
CSS Flex

Figma Layout Grid
        ↓
CSS Grid
```

완전히 1:1 대응은 아니지만 교육할 때 매우 유용한 연결입니다.

---

# 14. Figma Component와 HTML Component

Figma에서 버튼을 매번 새로 만들지 않고

```text
Button Component
```

를 만들어 재사용합니다.

웹에서도 비슷합니다.

단순 HTML/CSS에서는

```html
<button class="btn">로그인</button>

<button class="btn">회원가입</button>

<button class="btn">구매하기</button>
```

```css
.btn {
    padding: 10px 20px;
    border-radius: 6px;
}
```

처럼 CSS 클래스로 재사용할 수 있습니다.

React까지 가면 Figma Component 개념과 더 가까워집니다.

```jsx
<Button>로그인</Button>

<Button>회원가입</Button>

<Button>구매하기</Button>
```

따라서

```text
Figma Component
      ↓
HTML + CSS 재사용
      ↓
React Component
```

라는 흐름으로 설명하면 좋습니다.

---

# 15. Variant와 웹의 상태

Figma Component의 Variant를 이용하면

```text
Button

Default
Hover
Pressed
Disabled
```

같은 상태를 만들 수 있습니다.

CSS에서도

```css
button {
    background: blue;
}

button:hover {
    background: darkblue;
}

button:active {
    background: navy;
}

button:disabled {
    background: gray;
}
```

처럼 표현합니다.

따라서

```text
Figma Variant
       ↓
CSS 상태
       ↓
:hover
:active
:disabled
```

로 연결할 수 있습니다.

---

# 16. Prototype는 JavaScript와 관련이 큽니다

Figma에서 Prototype을 이용하여

```text
로그인 버튼 클릭
        ↓
로그인 화면 이동
```

을 만들었다고 하겠습니다.

이 부분은 CSS보다는 HTML/JavaScript와 관련이 있습니다.

가장 간단하게는

```html
<a href="login.html">로그인</a>
```

이고 JavaScript를 사용하면

```javascript
button.addEventListener("click", () => {
    location.href = "login.html";
});
```

처럼 구현할 수 있습니다.

따라서

```text
Figma Prototype
      ↓
HTML 링크
      +
JavaScript 이벤트
```

라고 보면 됩니다.

---

# 17. 실제 웹페이지 하나를 대응시켜 보면

Figma에서 다음 쇼핑몰 카드를 만들었다고 하겠습니다.

```text
┌────────────────────┐
│                    │
│      상품 이미지    │
│                    │
├────────────────────┤
│ 운동화             │
│ 59,000원           │
│                    │
│     [구매하기]      │
└────────────────────┘
```

Figma 구조를 생각하면

```text
Frame : Card

 ├ Image
 ├ Text : 운동화
 ├ Text : 59,000원
 └ Component : Button
```

HTML은

```html
<div class="card">

    <img src="shoe.jpg" alt="운동화">

    <h3>운동화</h3>

    <p>59,000원</p>

    <button>구매하기</button>

</div>
```

CSS는

```css
.card {
    width: 300px;
    padding: 20px;

    border: 1px solid #ddd;
    border-radius: 12px;

    box-shadow: 0 4px 10px rgba(0,0,0,0.1);
}

.card img {
    width: 100%;
}

.card button {
    width: 100%;
    padding: 10px;

    background-color: blue;
    color: white;

    border: none;
    border-radius: 6px;
}
```

입니다.

이 예에서 대응 관계를 보면 아주 명확합니다.

```text
Figma Frame
    ↓
HTML div

Figma Image
    ↓
HTML img

Figma Text
    ↓
HTML h3 / p

Figma Button Component
    ↓
HTML button

Figma Fill
    ↓
CSS background-color

Figma Stroke
    ↓
CSS border

Figma Radius
    ↓
CSS border-radius

Figma Shadow
    ↓
CSS box-shadow

Figma Width
    ↓
CSS width

Figma Padding
    ↓
CSS padding
```

---

# 18. 학생들에게 가장 중요한 개념

Figma를 배우고 HTML/CSS로 넘어갈 때 가장 중요한 것은 **“Figma 객체 하나 = HTML 태그 하나”라고 생각하지 않는 것**입니다.

예를 들어 Figma에서

```text
Frame
```

을 만들었다고 해서 반드시

```html
<div>
```

가 되는 것이 아닙니다.

내용의 의미에 따라서

```html
<header>
<nav>
<main>
<section>
<article>
<footer>
```

가 될 수 있습니다.

즉,

```text
Figma
    ↓
모양 중심

HTML
    ↓
구조 + 의미 중심

CSS
    ↓
디자인 + 배치 중심
```

이라는 차이가 있습니다.

---

# 19. 수업에서 가장 쉽게 설명하는 방법

저라면 비전공자 학생들에게 다음과 같이 설명하는 것을 추천합니다.

```text
Figma = 설계도

HTML = 건물의 골조

CSS = 인테리어

JavaScript = 움직이는 장치
```

예를 들어 로그인 버튼이라면

```text
Figma
"버튼을 어떻게 보이게 할 것인가?"

       ↓

HTML
"이것은 버튼이다."

<button>로그인</button>

       ↓

CSS
"버튼을 파란색, 둥근 모양으로 만든다."

       ↓

JavaScript
"버튼을 누르면 로그인 처리를 한다."
```

가 됩니다.

---

## 최종적으로 기억할 핵심 대응표

| Figma          | Web                              |
| -------------- | -------------------------------- |
| Frame          | HTML Container                   |
| Auto Layout    | CSS Flex                         |
| Layout Grid    | CSS Grid                         |
| Text           | `h1`, `p`, `span` 등              |
| Image          | `img`                            |
| Rectangle      | `div` + CSS                      |
| Fill           | `background-color`, `color`      |
| Stroke         | `border`                         |
| Radius         | `border-radius`                  |
| Shadow         | `box-shadow`                     |
| Padding        | `padding`                        |
| Gap            | `gap`                            |
| Alignment      | `justify-content`, `align-items` |
| Width / Height | `width`, `height`                |
| Hug            | `fit-content`                    |
| Fill Container | `width:100%`, `flex:1`           |
| Component      | 재사용 HTML / React Component       |
| Variant        | `:hover`, `:active`, 상태 클래스      |
| Constraints    | 반응형 CSS                          |
| Prototype      | HTML 링크 + JavaScript             |

**특히 Figma → HTML/CSS 수업에서는 `Frame → HTML 구조`, `Auto Layout → Flex`, `Layout Grid → Grid`, `Component → 재사용 UI` 이 네 가지를 중심으로 가르치면 학생들이 두 기술의 연결 관계를 가장 빨리 이해합니다.**
