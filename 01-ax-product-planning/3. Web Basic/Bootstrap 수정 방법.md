가장 효율적인 방법은 **Bootstrap을 그대로 쓰되, 필요한 부분만 덮어쓰는 방식**입니다. Bootstrap을 버리고 처음부터 CSS를 다시 작성하는 것이 아니라, **Bootstrap 80~90% + 사용자 정의 CSS 10~20%** 정도로 생각하면 좋습니다.

가장 일반적인 우선순위는 다음과 같습니다.

```text
1. Bootstrap 기본 클래스 사용
        ↓
2. Utility 클래스 조합
        ↓
3. 부족하면 사용자 CSS 추가
        ↓
4. 프로젝트 전체 테마를 바꿀 때는 Sass/Bootstrap 변수 수정
```

## 1. 가장 먼저 Bootstrap Utility를 조합한다

예를 들어 버튼이 너무 작다면 별도의 CSS를 만들기 전에 Bootstrap의 padding, font-size 등을 조합할 수 있습니다.

```html
<button class="btn btn-primary px-4 py-3 fs-5">
    구매하기
</button>
```

의미는:

```text
btn-primary → 기본 파란 버튼
px-4        → 좌우 padding
py-3        → 상하 padding
fs-5        → 글자 크기
```

즉, 가능한 경우에는 Bootstrap 클래스만 조합하는 것이 가장 간단합니다.

---

## 2. 원하는 스타일이 없다면 사용자 CSS를 추가한다

예를 들어 Bootstrap의 `btn-primary` 색상이 마음에 들지 않는다고 하겠습니다.

```html
<button class="btn btn-primary my-btn">
    구매하기
</button>
```

그리고 Bootstrap CSS를 불러온 **뒤에** 사용자 CSS를 작성합니다.

```html
<link
    href="bootstrap.min.css"
    rel="stylesheet"
>

<link
    href="style.css"
    rel="stylesheet"
>
```

`style.css`

```css
.my-btn {
    background-color: #6c4cff;
    border-color: #6c4cff;
    border-radius: 20px;
    font-size: 18px;
}
```

이 방식이 실무에서도 매우 일반적입니다.

핵심은:

```text
Bootstrap
   ↓
기본 스타일 제공

내 CSS
   ↓
필요한 부분만 수정
```

입니다.

---

# 3. Bootstrap 클래스를 직접 덮어쓰는 것도 가능하다

예를 들어:

```css
.btn-primary {
    background-color: purple;
    border-color: purple;
}
```

이렇게 하면 모든 `btn-primary` 버튼이 바뀝니다.

```html
<button class="btn btn-primary">저장</button>
<button class="btn btn-primary">구매</button>
<button class="btn btn-primary">확인</button>
```

모두 보라색으로 바뀝니다.

하지만 이 방식은 주의해야 합니다.

왜냐하면 프로젝트 전체의 `btn-primary`가 변경되기 때문입니다.

그래서 특정 버튼만 바꾸고 싶다면:

```css
.my-btn {
    background-color: purple;
}
```

처럼 **새 클래스를 추가하는 것이 더 안전합니다.**

---

# 4. Bootstrap + 사용자 class 조합이 가장 추천되는 방식

예를 들어 쇼핑몰 상품 카드가 있다고 하겠습니다.

Bootstrap만 사용:

```html
<div class="card">
    <div class="card-body">

        <h5 class="card-title">
            노트북
        </h5>

        <button class="btn btn-primary">
            구매하기
        </button>

    </div>
</div>
```

디자인을 조금 변경하고 싶다면:

```html
<div class="card product-card">

    <div class="card-body">

        <h5 class="card-title">
            노트북
        </h5>

        <button class="btn btn-primary product-btn">
            구매하기
        </button>

    </div>

</div>
```

```css
.product-card {
    border-radius: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.product-btn {
    background-color: #5c3df5;
    border: none;
}
```

이 구조가 상당히 좋습니다.

```text
Bootstrap
card
btn
        ↓
기본 구조와 기능

사용자 CSS
product-card
product-btn
        ↓
우리 서비스만의 디자인
```

---

# 5. 색상만 조금 변경하고 싶다면 CSS 변수를 활용할 수도 있다

Bootstrap 5에서는 CSS 변수를 많이 사용합니다.

예를 들어 버튼에서:

```css
.my-btn {
    --bs-btn-bg: #6f42c1;
    --bs-btn-border-color: #6f42c1;
}
```

```html
<button class="btn btn-primary my-btn">
    구매하기
</button>
```

이 방식의 장점은 Bootstrap의 내부 구조를 완전히 무시하지 않고, **Bootstrap이 제공하는 변수만 바꾼다는 것**입니다.

특히 hover, active 같은 상태가 있는 컴포넌트는 이런 방식이 편리할 수 있습니다.

---

# 6. 프로젝트 전체의 대표 색상을 바꿀 때는 Sass가 더 효율적이다

지금 SCSS를 먼저 배우고 Bootstrap을 배우는 이유가 여기서 연결됩니다.

예를 들어 회사의 대표색이:

```text
Bootstrap 기본 primary
파란색

↓ 변경

우리 서비스 primary
보라색
```

이라면 버튼마다 이렇게 작성하는 것은 비효율적입니다.

```css
.btn1 {
    background: purple;
}

.btn2 {
    background: purple;
}

.btn3 {
    background: purple;
}
```

Bootstrap을 Sass로 커스터마이징하면 기본 변수를 변경할 수 있습니다.

개념적으로는:

```scss
$primary: #6f42c1;
```

그 후 Bootstrap을 컴파일하면:

```text
btn-primary
text-primary
bg-primary
border-primary
```

등이 모두 새로운 `primary` 색상을 기준으로 만들어집니다.

즉,

```text
Bootstrap 기본 테마

primary = blue
success = green
danger  = red

        ↓ Sass 설정

primary = purple

        ↓

전체 Bootstrap 스타일 생성
```

입니다.

---

# 7. 크기가 맞지 않는 경우도 같은 방식이다

예를 들어 카드의 너비를 Bootstrap Utility로 해결할 수 있다면:

```html
<div class="card w-50">
```

사용합니다.

그런데 정확히 `350px`이어야 한다면 Bootstrap에 그런 클래스가 없을 수 있습니다.

그럴 때는:

```html
<div class="card product-card">
```

```css
.product-card {
    width: 350px;
}
```

처럼 작성하는 것이 훨씬 낫습니다.

억지로 Bootstrap 클래스만 사용하려고 할 필요는 없습니다.

---

# 8. Bootstrap을 사용할 때 가장 피해야 할 방법

다음과 같은 방식은 권장하지 않습니다.

```html
<div style="
    width: 347px;
    background-color: #683df2;
    margin-top: 17px;
    padding: 13px;
">
```

즉, 지나친 inline style입니다.

작은 테스트에는 괜찮지만 프로젝트가 커지면 관리가 어려워집니다.

차라리:

```html
<div class="product-box">
```

```css
.product-box {
    width: 347px;
    background-color: #683df2;
    margin-top: 17px;
    padding: 13px;
}
```

가 좋습니다.

---

# 9. `!important`는 가능하면 마지막 수단으로 사용한다

초보자가 Bootstrap 스타일이 안 바뀌면 자주 이렇게 합니다.

```css
.my-btn {
    background-color: purple !important;
}
```

물론 동작할 수 있습니다.

하지만 계속 사용하다 보면 나중에는:

```css
!important
```

끼리 충돌하게 됩니다.

따라서 우선:

```css
.my-btn {
    background-color: purple;
}
```

를 사용하고, 선택자 우선순위와 CSS 로딩 순서를 확인하는 것이 좋습니다.

특히 다음 순서가 중요합니다.

```html
<!-- 먼저 Bootstrap -->

<link href="bootstrap.min.css" rel="stylesheet">

<!-- 나중에 내 CSS -->

<link href="style.css" rel="stylesheet">
```

CSS는 일반적으로 **뒤에 선언된 스타일이 같은 우선순위에서는 나중 값을 적용**하기 때문입니다.

---

# 10. 실무적으로 가장 좋은 기준

학생들에게는 다음 기준으로 가르치면 이해하기 쉽습니다.

| 상황                  | 추천 방법                  |
| ------------------- | ---------------------- |
| 간단한 margin/padding  | Bootstrap Utility      |
| 정렬                  | Bootstrap Flex Utility |
| 기본 색상               | Bootstrap 색상 클래스       |
| 정확한 색상 필요           | 사용자 CSS                |
| 정확한 width/height 필요 | 사용자 CSS                |
| 특정 컴포넌트만 변경         | 사용자 class 추가           |
| 전체 버튼 색상 변경         | Bootstrap 클래스 override |
| 전체 프로젝트 테마 변경       | Sass 변수                |
| 간단한 일회성 테스트         | inline style 가능        |
| 강제 적용               | `!important`는 마지막 수단   |

결국 Bootstrap의 가장 좋은 사용 방식은 다음입니다.

```text
Bootstrap이 제공한다
        ↓
그대로 사용


Bootstrap이 비슷하게 제공한다
        ↓
Utility 조합


Bootstrap에 없다
        ↓
내 CSS 작성


프로젝트 전체 디자인이 다르다
        ↓
Sass / Bootstrap 변수 수정
```

따라서 **Bootstrap을 쓰면 CSS를 안 써도 된다**가 아니라,

> **Bootstrap으로 공통적인 CSS 작업을 줄이고, 서비스 고유의 디자인만 직접 CSS/SCSS로 작성한다**

라고 이해하는 것이 가장 정확합니다.

특히 수업에서는 `Bootstrap 기본 카드 → Utility로 수정 → 사용자 CSS로 수정 → SCSS로 전체 테마 변경` 순서의 한 가지 예제를 보여주면, HTML → CSS → SCSS → Bootstrap을 왜 순서대로 배웠는지가 학생들에게 한 번에 연결됩니다.
