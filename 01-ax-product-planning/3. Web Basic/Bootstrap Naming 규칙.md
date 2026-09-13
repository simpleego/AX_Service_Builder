부트스트랩의 CSS 네이밍 규칙은 처음에는 클래스 이름이 많아 보여 복잡하지만, 실제로는 **“무엇을(property) + 어디에(side/breakpoint) + 어느 정도(value)”**라는 규칙을 이해하면 대부분 해석할 수 있습니다.

특히 Bootstrap 5.x 기준으로는 Utility 클래스의 상당수가 다음 구조를 따릅니다.

```text
기능 - 방향 - 반응형기준 - 값
```

예를 들어:

```html
mt-md-3
```

는 다음처럼 읽습니다.

```text
m   t   md   3
│   │   │    │
│   │   │    └─ 크기
│   │   └────── medium 이상
│   └────────── top
└────────────── margin
```

Bootstrap 공식 문서도 spacing utility를 `{property}{sides}-{size}` 또는 `{property}{sides}-{breakpoint}-{size}` 형태로 정의합니다. ([부트스트랩][1])

## 1. 가장 기본적인 네이밍 원칙

Bootstrap 클래스는 대부분 **소문자 + 하이픈(-)** 형태입니다.

```html
btn-primary
text-center
bg-danger
justify-content-center
align-items-center
```

따라서 일반적으로 다음과 같은 형태를 사용하지 않습니다.

```text
btnPrimary      ← camelCase X
BtnPrimary      ← PascalCase X
btn_primary     ← snake_case X
```

기본 형태는:

```text
btn-primary
```

입니다.

---

# 2. 가장 중요한 규칙: 속성-값

가장 간단한 형태는 다음입니다.

```text
속성-값
```

예를 들어 CSS가:

```css
display: flex;
```

라면 Bootstrap에서는:

```html
<div class="d-flex">
```

입니다.

여기서:

```text
d      = display
flex   = flex
```

즉:

```text
d-flex
│ │
│ └── flex
└──── display
```

공식적으로 display utility는 `.d-{value}` 형식을 사용합니다. ([부트스트랩][2])

다른 예도 비슷합니다.

```text
d-block
d-none
d-grid
d-flex
```

의미는:

```css
display: block;
display: none;
display: grid;
display: flex;
```

입니다.

---

# 3. Margin과 Padding 네이밍 규칙

Bootstrap에서 가장 중요한 네이밍 규칙입니다.

기본 구조:

```text
{property}{side}-{size}
```

### property

```text
m = margin
p = padding
```

따라서:

```html
m-3
```

는

```css
margin: ...;
```

이고,

```html
p-3
```

는

```css
padding: ...;
```

입니다. ([부트스트랩][1])

---

# 4. 방향은 한 글자로 표현한다

```text
t = top
b = bottom

s = start
e = end

x = 좌우
y = 상하
```

따라서:

```text
mt-3
```

는

```text
margin-top
```

이고,

```text
pb-2
```

는

```text
padding-bottom
```

입니다.

전체적으로 보면:

| Bootstrap | 의미            |
| --------- | ------------- |
| `m-3`     | margin 전체     |
| `mt-3`    | margin-top    |
| `mb-3`    | margin-bottom |
| `ms-3`    | margin-start  |
| `me-3`    | margin-end    |
| `mx-3`    | 좌우 margin     |
| `my-3`    | 상하 margin     |
| `p-3`     | padding 전체    |
| `pt-3`    | padding-top   |
| `px-3`    | 좌우 padding    |
| `py-3`    | 상하 padding    |

여기서 Bootstrap 5에서는 `left/right` 대신 **start/end** 개념을 사용합니다. LTR 언어에서는 `start`가 왼쪽, `end`가 오른쪽이지만 RTL 언어에서는 반대가 될 수 있기 때문입니다. ([부트스트랩][1])

---

# 5. 숫자는 실제 px 값이 아니다

초보자가 많이 오해하는 부분입니다.

```html
<div class="mt-3">
```

에서 `3`은

```css
margin-top: 3px;
```

이라는 뜻이 아닙니다.

Bootstrap이 미리 정의한 **spacing scale의 단계 번호**입니다.

기본적으로:

```text
0
1
2
3
4
5
```

와 같은 단계가 있습니다.

따라서 학생들에게는 처음에는 다음 정도로 이해시키는 것이 좋습니다.

```text
0 → 없음
1 → 매우 작음
2 → 작음
3 → 보통
4 → 큼
5 → 매우 큼
```

Bootstrap의 기본 spacing 값은 Sass의 `$spacers` 맵에서 관리됩니다. ([부트스트랩][1])

---

# 6. 반응형 클래스 네이밍 규칙

Bootstrap에서 매우 중요한 규칙입니다.

기본 구조:

```text
속성-화면크기-값
```

예를 들어:

```html
d-md-flex
```

는:

```text
d     md      flex
│      │       │
│      │       └─ flex
│      └──────── medium 이상
└─────────────── display
```

즉:

> 화면 너비가 `md` 이상일 때 `display:flex`

라는 뜻입니다.

공식적인 형식도 `.d-{breakpoint}-{value}`입니다. ([부트스트랩][2])

---

# 7. Bootstrap의 화면 크기 약어

Bootstrap 5.3 기준 기본 breakpoint는 다음과 같습니다. ([부트스트랩][3])

| 약어    | 의미                |        기준 |
| ----- | ----------------- | --------: |
| 없음    | Extra Small       |    0px 이상 |
| `sm`  | Small             |  576px 이상 |
| `md`  | Medium            |  768px 이상 |
| `lg`  | Large             |  992px 이상 |
| `xl`  | Extra Large       | 1200px 이상 |
| `xxl` | Extra Extra Large | 1400px 이상 |

예를 들어:

```html
<div class="d-none d-md-block">
```

는:

```text
d-none
→ 기본적으로 숨김

d-md-block
→ md(768px) 이상에서는 block
```

즉:

```text
모바일     숨김
태블릿↑    표시
```

입니다.

---

# 8. Grid 클래스의 네이밍

Grid 역시 규칙이 명확합니다.

```text
col-{개수}
```

예:

```html
<div class="col-6">
```

의미:

```text
12칸 중 6칸
→ 50%
```

반응형까지 포함하면:

```text
col-{breakpoint}-{개수}
```

예:

```html
<div class="col-md-6">
```

해석:

```text
col
 ↓
column

md
 ↓
768px 이상

6
 ↓
12칸 중 6칸
```

따라서:

```html
<div class="col-12 col-md-6 col-lg-4">
```

는 매우 중요한 예제입니다.

```text
모바일        col-12 → 1개씩
                 ↓
태블릿        col-md-6 → 2개씩
                 ↓
데스크탑      col-lg-4 → 3개씩
```

---

# 9. 색상은 의미 중심으로 네이밍한다

Bootstrap 색상은 단순히 `blue`, `red`라고 하지 않고 **의미(Semantic)**를 사용합니다.

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
<button class="btn btn-primary">저장</button>

<button class="btn btn-danger">삭제</button>
```

여기서:

```text
btn
→ 버튼이라는 Component

btn-primary
→ primary 스타일의 버튼
```

입니다.

같은 의미 이름이 여러 기능에 반복됩니다.

```html
text-primary

bg-primary

border-primary

btn-primary
```

따라서:

```text
primary
```

자체를 하나의 공통적인 **의미 색상 토큰**이라고 이해하면 좋습니다.

---

# 10. Text 클래스 네이밍

다음 패턴을 많이 사용합니다.

```text
text-{값}
```

예:

```html
text-center
text-start
text-end
```

CSS로 보면:

```css
text-align: center;
text-align: start;
text-align: end;
```

색상 역시:

```html
text-primary
text-danger
text-success
text-muted
```

처럼 사용합니다.

---

# 11. Background

규칙:

```text
bg-{값}
```

예:

```html
bg-primary
bg-danger
bg-dark
bg-light
```

따라서:

```html
<div class="bg-dark text-white">
```

처럼 조합할 수 있습니다.

Bootstrap을 사용할 때 중요한 특징은 **하나의 거대한 클래스를 사용하는 것이 아니라 여러 작은 Utility 클래스를 조합한다는 것**입니다.

---

# 12. Border

규칙 역시 직관적입니다.

```text
border
border-{방향}
border-{색상}
border-{크기}
```

예:

```html
border
border-top
border-bottom
border-primary
border-danger
```

둥근 모서리는:

```html
rounded
rounded-circle
rounded-pill
```

과 같이 사용합니다.

---

# 13. Flex 네이밍

Bootstrap을 사용할 때 가장 많이 접하는 부분입니다.

CSS:

```css
display: flex;
```

Bootstrap:

```html
d-flex
```

CSS:

```css
justify-content: center;
```

Bootstrap:

```html
justify-content-center
```

CSS:

```css
align-items: center;
```

Bootstrap:

```html
align-items-center
```

따라서 Bootstrap 클래스 이름을 보면 원래 CSS 속성이 상당히 그대로 보입니다.

```text
justify-content-between

justify-content-center

align-items-start

align-items-center

flex-row

flex-column
```

이 점을 학생들에게 강조하면 Bootstrap 암기가 크게 줄어듭니다.

---

# 14. 크기 관련 네이밍

Width:

```text
w-{값}
```

예:

```html
w-25
w-50
w-75
w-100
```

Height:

```text
h-{값}
```

예:

```html
h-25
h-50
h-100
```

예:

```html
<div class="w-50">
```

는 대략:

```css
width: 50%;
```

라는 의미입니다.

---

# 15. Component의 네이밍은 조금 다르다

지금까지 설명한 것은 주로 **Utility 클래스**입니다.

Bootstrap에는 Component 클래스도 있습니다.

예를 들어 Button:

```html
<button class="btn btn-primary">
```

Card:

```html
<div class="card">
    <div class="card-body">
        <h5 class="card-title">
```

Navbar:

```html
<nav class="navbar">
```

Alert:

```html
<div class="alert alert-danger">
```

이런 Component는 보통:

```text
컴포넌트 이름

        +

컴포넌트-세부요소

        +

컴포넌트-변형
```

구조입니다.

예를 들어 Card:

```text
card
card-body
card-title
card-text
card-header
card-footer
```

Button:

```text
btn
btn-primary
btn-danger
btn-outline-primary
```

Alert:

```text
alert
alert-primary
alert-danger
```

---

# 16. Utility와 Component를 구분하면 Bootstrap이 쉬워진다

학생들에게 저는 이 구분을 특히 강조할 것을 권합니다.

### Utility

CSS 속성을 간단하게 표현합니다.

```text
mt-3
p-2
d-flex
text-center
bg-dark
w-100
```

즉:

```text
CSS 속성 → Bootstrap 짧은 클래스
```

### Component

완성된 UI 부품입니다.

```text
btn
card
navbar
alert
modal
accordion
```

즉:

```text
여러 CSS 스타일의 묶음
        ↓
완성된 UI Component
```

---

# 17. 네이밍 규칙을 하나의 공식으로 정리하면

Bootstrap Utility는 대체로 다음처럼 생각할 수 있습니다.

```text
[무엇을]-[어디서]-[어떤 값으로]
```

조금 더 정확하게 표현하면:

```text
property
   ↓
side
   ↓
breakpoint
   ↓
value
```

예:

```text
mt-md-5
```

분해하면:

```text
m        t        md        5
│        │         │        │
margin   top     768px↑    크기
```

따라서 학생들에게 Bootstrap 클래스 이름을 **외우지 말고 분해해서 읽도록** 가르치는 것이 좋습니다.

---

## 18. 수업에서 먼저 익히면 좋은 클래스 20개

처음 Bootstrap을 배우는 학생이라면 다음 정도만 먼저 익히면 충분합니다.

```text
container
row
col

col-12
col-md-6
col-lg-4

m-3
mt-3
mb-3
p-3

d-flex
d-block
d-none

justify-content-center
align-items-center

text-center
text-primary

bg-light
bg-dark

btn
btn-primary

card
form-control
```

이 정도를 이해한 다음 새로운 클래스를 볼 때,

```html
<div class="d-lg-flex justify-content-between mt-4 p-3">
```

를 다음처럼 읽을 수 있어야 합니다.

```text
d-lg-flex
→ lg 이상에서 flex

justify-content-between
→ 양쪽으로 벌려 배치

mt-4
→ 위쪽 margin 4단계

p-3
→ 전체 padding 3단계
```

이 능력이 생기면 Bootstrap은 사실상 **“새로운 CSS를 배우는 것”이 아니라 “CSS 속성을 Bootstrap의 축약 네이밍으로 읽는 것”**으로 바뀝니다. 이것이 비전공자에게 Bootstrap을 가르칠 때 가장 중요한 포인트입니다.

[1]: https://getbootstrap.com/docs/5.3/utilities/spacing/?utm_source=chatgpt.com "Spacing · Bootstrap v5.3"
[2]: https://getbootstrap.com/docs/5.3/utilities/display/?utm_source=chatgpt.com "Display property · Bootstrap v5.3"
[3]: https://getbootstrap.com/docs/5.3/layout/breakpoints/?utm_source=chatgpt.com "Breakpoints · Bootstrap v5.3"
