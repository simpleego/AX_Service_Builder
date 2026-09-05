# CSS 레이아웃 완전 정리 — 과거에서 현재까지, 그리고 Flex vs Grid

- **대상**: 웹개발 입문 비전공자 (HTML/CSS 기초 학습 후)  
- **목표**: ① CSS 배치 기술이 왜, 어떻게 발전해왔는지 흐름을 이해하고 ② Flexbox와 Grid를 상황에 맞게 선택할 수 있는 판단력을 학습
- **왜 역사를 배우나?**: 실무 코드와 AI가 생성한 코드에는 옛날 방식과 현대 방식이 섞여 있습니다. "이건 옛날 방식이니 이렇게 고치자"라고 판단하려면 발전 과정을 숙지 

---

# 1부. CSS 레이아웃의 발전사 — "박스를 어떻게 원하는 위치에 놓을 것인가"

CSS 레이아웃의 역사는 한 문장으로 요약됩니다.

> **"원래 배치용이 아니었던 기능을 억지로 쓰다가 → 마침내 배치 전용 도구를 얻기까지"**

```
1990년대          2000년대           2012~              2017~              현재
┌──────────┐   ┌──────────────┐   ┌──────────┐   ┌──────────┐   ┌─────────────────┐
│ table    │ → │ float        │ → │ Flexbox  │ → │ Grid     │ → │ Flex + Grid 조합 │
│ 배치     │   │ + position   │   │ (1차원)  │   │ (2차원)  │   │ + gap, 컨테이너   │
│ (표 남용)│   │ (꼼수의 시대)│   │          │   │          │   │   쿼리 등        │
└──────────┘   └──────────────┘   └──────────┘   └──────────┘   └─────────────────┘
```

---

## 1-1. 태초의 흐름: Normal Flow (기본 배치 규칙)

모든 레이아웃 기술의 출발점입니다. CSS를 아무것도 안 쓰면 브라우저는 이 규칙대로 배치합니다.

```html
<div>블록 요소 1</div>   <!-- 한 줄을 통째로 차지 → 세로로 쌓임 -->
<div>블록 요소 2</div>
<span>인라인 1</span>    <!-- 내용만큼만 차지 → 가로로 이어짐 -->
<span>인라인 2</span>
```

| 구분 | 특징 | 대표 태그 |
|------|------|-----------|
| **블록(block)** | 한 줄 전체 차지, 위→아래로 쌓임, width/height 지정 가능 | `div`, `p`, `h1`, `section` |
| **인라인(inline)** | 내용 크기만큼 차지, 좌→우로 흐름, width/height 지정 불가 | `span`, `a`, `strong` |

> 💡 **핵심**: "블록은 세로로, 인라인은 가로로." 이 기본 흐름을 **어떻게 거스르고 제어하느냐**가 레이아웃 기술의 역사입니다.

---

## 1-2. 1990년대: `<table>` 배치의 시대 (흑역사)

레이아웃 도구가 없던 시절, 개발자들은 **표(table) 태그로 페이지 전체를 짰습니다.**

```html
<!-- ❌ 1990년대 방식: 절대 따라하지 마세요 -->
<table>
    <tr>
        <td colspan="2">헤더</td>
    </tr>
    <tr>
        <td>사이드바</td>
        <td>본문</td>
    </tr>
</table>
```

**문제점**: 표는 "데이터를 담는 의미"의 태그인데 배치용으로 남용 → 구조와 디자인이 뒤엉킴, 유지보수 지옥, 접근성 최악.

> 💡 **교훈**: 여기서 나온 반성이 바로 **"구조(HTML)와 표현(CSS)의 분리"** 원칙입니다. `<table>`은 지금도 "진짜 표 데이터"에만 사용합니다.

---

## 1-3. 2000년대: `float` — 꼼수의 전성기

`float`는 원래 **신문처럼 이미지 주위로 글자를 흐르게** 하려고 만든 기능입니다.

```css
/* float의 원래 용도: 이미지 옆으로 텍스트가 감싸며 흐름 */
img {
    float: left;        /* 이미지를 왼쪽으로 띄우고 */
    margin-right: 12px; /* 글자와의 간격 */
}
```

그런데 "요소를 옆으로 나란히 놓을 수 있다"는 점 때문에 **레이아웃 도구로 남용**되었습니다.

```css
/* ❌ 2000년대 방식: float로 2단 레이아웃 만들기 */
.sidebar { float: left;  width: 30%; }
.content { float: right; width: 70%; }

/* float의 고질병: 부모가 자식 높이를 인식 못 함 → clearfix 꼼수 필요 */
.container::after {
    content: "";
    display: block;
    clear: both;    /* float 해제 마법의 주문 */
}
```

**문제점**: 세로 중앙 정렬이 사실상 불가능, `clearfix` 같은 꼼수 코드 필수, 요소 하나가 어긋나면 전체가 무너짐.

> 💡 **지금은?**: float는 **원래 용도(텍스트 감싸기)로만** 사용합니다. 오래된 코드나 AI가 가끔 생성하는 구식 코드에서 `float` 레이아웃을 보면 → Flexbox/Grid로 리팩토링 대상입니다.

---

## 1-4. 같은 시대의 도구들: `position`과 `inline-block`

### position — "좌표로 콕 집어 배치"

```css
/* relative: 원래 자리를 기준으로 살짝 이동 (기준점 역할로 자주 씀) */
.parent { position: relative; }

/* absolute: 가장 가까운 position 지정 조상을 기준으로 좌표 배치 */
.badge {
    position: absolute;
    top: 8px;
    right: 8px;      /* 부모의 오른쪽 위 모서리에 붙임 */
}

/* fixed: 스크롤해도 화면에 고정 (예: 상단 고정 내비게이션) */
.navbar {
    position: fixed;
    top: 0;
    width: 100%;
}

/* sticky: 평소엔 흐름대로, 스크롤이 닿으면 고정 (현대에 추가됨) */
.section-title {
    position: sticky;
    top: 0;
}
```

**한계**: 좌표 배치는 강력하지만, **전체 레이아웃을 position으로 짜면** 화면 크기가 바뀔 때 다 깨집니다.

> 💡 **현대의 역할**: position은 레이아웃의 주인공이 아니라 **"특수 배치 담당"**입니다. 뱃지, 툴팁, 고정 헤더, 모달처럼 "흐름에서 벗어나야 하는 요소"에만 사용합니다. `relative(기준) + absolute(배치)` 콤보는 지금도 실무 필수 패턴입니다.

### inline-block — 과도기의 타협안

```css
/* 블록처럼 크기를 갖되, 인라인처럼 가로로 나열 */
.menu-item {
    display: inline-block;
    width: 100px;
}
```

**한계**: 요소 사이에 HTML 공백 문자만큼 의문의 틈이 생기는 등 미세 제어가 어려움 → Flexbox 등장 후 레이아웃 용도로는 거의 사용하지 않습니다.

---

## 1-5. 2012~: Flexbox — 드디어 등장한 "배치 전용" 도구 (1차원)

**"한 방향(행 또는 열)으로 요소들을 유연하게 배치"**하기 위해 태어난 최초의 진짜 레이아웃 도구입니다.

```css
.container {
    display: flex;                 /* 자식들이 flex 아이템이 됨 */
    flex-direction: row;           /* 주축 방향: row(가로, 기본) | column(세로) */
    justify-content: space-between;/* 주축 정렬: 양 끝 배치 */
    align-items: center;           /* 교차축 정렬: 세로 중앙 */
    gap: 16px;                     /* 아이템 간격 (float 시절엔 꿈같던 기능) */
    flex-wrap: wrap;               /* 공간 부족 시 줄바꿈 허용 */
}
```

**핵심 개념 — 주축과 교차축:**

```
flex-direction: row (기본)          flex-direction: column
─────────────────────▶ 주축         │
[아이템][아이템][아이템]             │ 주축      [아이템]
│                                   │           [아이템]
▼ 교차축                            ▼           [아이템]
```

- `justify-content` → **주축** 방향 정렬 (기본: 가로)
- `align-items` → **교차축** 방향 정렬 (기본: 세로)
- `flex-direction`을 바꾸면 두 속성의 방향도 함께 바뀝니다 (혼동 최다 포인트!)

**자식(아이템) 쪽 핵심 속성:**

```css
.item {
    flex: 1;          /* 남는 공간을 균등하게 나눠 가짐 */
}
.item-fixed {
    flex: 0 0 200px;  /* 늘지도 줄지도 않는 고정 200px (사이드바 등) */
}
```

**float 시절의 난제가 한 줄로 해결된 예 — 세로 중앙 정렬:**

```css
/* float 시대: 사실상 불가능에 가까운 꼼수 필요 → Flexbox: 3줄 */
.center {
    display: flex;
    justify-content: center;
    align-items: center;
}
```

---

## 1-6. 2017~: Grid — 2차원 레이아웃의 완성

Flexbox가 "한 줄"을 다룬다면, Grid는 **행과 열을 동시에** 다룹니다. 드디어 "페이지 전체 판짜기"가 CSS 문법으로 가능해졌습니다.

```css
.page {
    display: grid;
    grid-template-columns: 200px 1fr;      /* 열: 고정 200px + 나머지 전부(1fr) */
    grid-template-rows: 60px 1fr 40px;     /* 행: 헤더 60px, 본문 유동, 푸터 40px */
    gap: 16px;
    min-height: 100vh;
}
```

**Grid의 꽃 — 영역에 이름 붙여 배치하기 (`grid-template-areas`):**

```css
.page {
    display: grid;
    grid-template-columns: 200px 1fr;
    grid-template-rows: 60px 1fr 40px;
    /* 레이아웃을 "그림 그리듯" 선언 — 코드만 봐도 화면 구조가 보임! */
    grid-template-areas:
        "header header"
        "sidebar main"
        "footer footer";
}
.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

```
결과 화면:
┌─────────────────────────┐
│         header          │
├────────┬────────────────┤
│sidebar │      main      │
├────────┴────────────────┤
│         footer          │
└─────────────────────────┘
```

**반복과 반응형을 한 줄로 — 실무 최강 패턴:**

```css
/* 카드 목록: 최소 250px을 지키며, 들어갈 수 있는 만큼 자동 배치 */
.card-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}
/* 미디어 쿼리 없이도 화면이 좁아지면 자동으로 열 수가 줄어듦! */
```

> 💡 **단위 `fr`**: "fraction(비율)"의 약자. `1fr 2fr`는 남는 공간을 1:2로 나눈다는 뜻. Grid에서만 쓰는 전용 단위입니다.

---

## 1-7. 현재: 그리고 계속 발전 중

| 기능 | 설명 |
|------|------|
| `gap` | 원래 Grid 전용이었으나 이제 **Flexbox에서도 사용 가능** (margin 꼼수 종말) |
| `aspect-ratio` | 가로세로 비율 고정 (`aspect-ratio: 16 / 9;`) — 영상/썸네일 배치 간소화 |
| **컨테이너 쿼리** `@container` | 화면 크기가 아니라 **부모 요소 크기** 기준 반응형 — 컴포넌트 시대의 반응형 |
| `subgrid` | 자식 그리드가 부모의 행/열 선을 이어받음 — 카드 내부 정렬 문제 해결 |

```css
/* 컨테이너 쿼리 맛보기: "이 카드가 놓인 공간이 400px 이하면" */
.card-wrapper { container-type: inline-size; }

@container (max-width: 400px) {
    .card { flex-direction: column; }   /* 화면이 아닌 '자리' 기준으로 변신 */
}
```

> 💡 **흐름 읽기**: 발전 방향은 일관됩니다 — "꼼수 제거", "선언만 하면 브라우저가 알아서", "페이지 단위 → 컴포넌트 단위". 이 방향성을 알면 새 기능이 나와도 빠르게 이해할 수 있습니다.

---

# 2부. Flexbox vs Grid — 언제 무엇을 쓸 것인가

## 2-1. 한 장 비교표

| 구분 | **Flexbox** | **Grid** |
|------|-------------|----------|
| 차원 | **1차원** (행 *또는* 열, 한 방향) | **2차원** (행 *과* 열, 동시 제어) |
| 사고방식 | **콘텐츠 중심**: 내용물이 흐르다가 공간에 맞게 유연히 조절 | **레이아웃 중심**: 판을 먼저 짜고 내용물을 칸에 배치 |
| 설계 주체 | 아이템(자식)이 스스로 늘고 줄어듦 | 컨테이너(부모)가 구조를 결정 |
| 줄 간 정렬 | `wrap`으로 줄바꿈 시 **줄끼리 열이 안 맞음** | 행/열이 격자로 **항상 정렬됨** |
| 대표 용도 | 내비게이션 바, 버튼 그룹, 카드 내부 정렬 | 페이지 전체 골격, 갤러리, 대시보드 |
| 겹치기 | 어려움 | `grid-area` 지정으로 쉬움 |

## 2-2. 판단 기준 — 3가지 질문

코드를 쓰기 전에 스스로 물어보세요.

```
Q1. "한 줄(한 방향)로 늘어놓는 건가?"          → 예: Flexbox
Q2. "행과 열이 모두 있는 격자 구조인가?"        → 예: Grid
Q3. "내용물 크기에 맞춰 유연하게? (콘텐츠 우선)  → Flexbox
     아니면 판을 먼저 짜고 채워넣기? (구조 우선)" → Grid
```

## 2-3. 사례로 익히는 선택 기준

### ✅ Flexbox가 어울리는 경우

**① 내비게이션 바** — 로고는 왼쪽, 메뉴는 오른쪽 (한 줄, 콘텐츠 크기 제각각)

```css
.navbar {
    display: flex;
    justify-content: space-between;  /* 양 끝으로 밀어내기 */
    align-items: center;
}
```

**② 버튼/태그 그룹** — 개수가 유동적이고 그냥 흐르면 되는 것들

```css
.tag-list {
    display: flex;
    flex-wrap: wrap;   /* 넘치면 자연스럽게 다음 줄로 */
    gap: 8px;
}
```

**③ 카드 내부 정렬** — 아이콘 + 텍스트 + 버튼을 한 줄에

```css
.card-row {
    display: flex;
    align-items: center;
    gap: 12px;
}
```

### ✅ Grid가 어울리는 경우

**① 페이지 전체 골격** — 헤더/사이드바/본문/푸터 (전형적인 2차원)

```css
/* 1-6의 grid-template-areas 예제가 바로 이 경우 */
```

**② 이미지 갤러리 / 상품 목록** — 줄이 바뀌어도 열이 딱딱 맞아야 함

```css
.gallery {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
}
/* Flexbox + wrap으로 만들면 마지막 줄 아이템 크기가 제멋대로가 됨
   → 격자가 필요하면 Grid! */
```

**③ 대시보드** — 위젯마다 차지하는 칸 수가 다른 복잡한 화면

```css
.dashboard {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
}
.big-widget {
    grid-column: span 2;   /* 가로 2칸 차지 */
    grid-row: span 2;      /* 세로 2칸 차지 */
}
```

## 2-4. 실무의 정답: "vs"가 아니라 "함께"

실전에서는 **Grid로 큰 판을 짜고, 각 칸 안은 Flexbox로 정렬**하는 조합이 표준입니다.

```css
/* [바깥] Grid: 페이지 골격 */
.page {
    display: grid;
    grid-template-columns: 240px 1fr;
    grid-template-areas:
        "sidebar header"
        "sidebar main";
}

/* [안쪽] Flexbox: 헤더 내부의 한 줄 정렬 */
.header {
    grid-area: header;
    display: flex;                   /* Grid의 칸 안에서 Flex 사용 */
    justify-content: space-between;
    align-items: center;
}

/* [안쪽] Grid: 본문 안의 카드 격자 */
.main {
    grid-area: main;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
}

/* [더 안쪽] Flexbox: 카드 하나 내부의 세로 배치 */
.card {
    display: flex;
    flex-direction: column;
    gap: 8px;
}
```

```
페이지(Grid)
┌─────────┬──────────────────────────────┐
│         │  헤더(Flex): 제목 ↔ 프로필    │
│ 사이드바 ├──────────────────────────────┤
│         │  본문(Grid): 카드 격자        │
│         │  ┌──────┐ ┌──────┐ ┌──────┐ │
│         │  │카드  │ │카드  │ │카드  │ │  ← 카드 내부는 Flex(column)
│         │  └──────┘ └──────┘ └──────┘ │
└─────────┴──────────────────────────────┘
```

---

# 3부. 정리

## 발전사 한눈에 보기

| 시대 | 도구 | 본래 용도 | 현재 위상 |
|------|------|-----------|-----------|
| 1990s | `table` | 표 데이터 | ❌ 레이아웃 사용 금지, 표에만 |
| 2000s | `float` | 텍스트 감싸기 | ⚠️ 원래 용도로만 |
| 2000s | `position` | 좌표 배치 | ✅ 특수 배치(뱃지·모달·고정헤더) 담당 |
| 2000s | `inline-block` | 과도기 타협 | ⚠️ 레이아웃 용도론 거의 안 씀 |
| 2012~ | `Flexbox` | **1차원 배치 전용** | ✅ 현역 주력 |
| 2017~ | `Grid` | **2차원 배치 전용** | ✅ 현역 주력 |
| 현재 | `gap`·`@container` 등 | 다듬기와 확장 | ✅ 계속 발전 중 |

## 선택 기준 한 줄 요약

> **"한 방향으로 흐르면 Flex, 행과 열의 격자면 Grid, 실무에선 Grid로 판 짜고 Flex로 채운다."**

## AI 시대 관점의 체크포인트

- AI가 생성한 CSS에 `float` 레이아웃이나 과도한 `position: absolute`가 보이면 → **구식 패턴, Flex/Grid로 교체 요청**할 수 있어야 합니다.
- "이 화면을 만들어줘"보다 **"Grid로 2열 골격을 잡고 카드 목록은 auto-fill minmax로"**라고 말할 수 있는 어휘력이 곧 AI 활용 능력입니다.
- 브라우저 개발자 도구(F12)에서 flex/grid 뱃지를 클릭하면 **격자선이 시각화**됩니다 — 디버깅 필수 습관!
