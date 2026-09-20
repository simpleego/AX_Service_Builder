# 피그마와 HTML/CSS 구조 이해
> 피그마(Figma)에서 디자인하는 시각적 요소들은 웹 표준인 HTML(구조)과 CSS(스타일 및 레이아웃)의 개념과 1:1로 매칭됩니다.  
> 피그마의 주요 구성 요소가 HTML/CSS에서 어떤 역할과 코드로 변환되는지 정리해 드립니다.

---

### 1. 구조와 태그 (Figma 요소 $\rightarrow$ HTML)

피그마의 레이어와 오브젝트는 웹페이지의 뼈대를 이루는 HTML 태그로 구조화됩니다.

* **Frame / Group (프레임 / 그룹)**: HTML의 **`<div>`, `<section>`, `<article>**` 같은 컨테이너 태그 역할을 합니다. 특히 '프레임(Frame)'은 실제 웹의 컨테이너 박스 모델과 거의 동일하게 작동합니다.
* **Text (텍스트)**: HTML의 텍스트 관련 태그인 **`<h1>`~`<h6>`, `<p>`, `<span>**` 등으로 변환됩니다.
* **Rectangle / Shape (사각형 및 도형)**: **`<div>`** 태그나 아이콘/일러스트의 경우 **`<svg>`** 코드로 변환됩니다.
* **Image (이미지)**: HTML의 **`<img>`** 태그 또는 CSS의 `background-image` 속성이 됩니다.
* **Component / Instance (컴포넌트)**: 프론트엔드 프레임워크(React, Vue 등)에서 사용하는 **재사용 가능한 컴포넌트(Component)** 구조와 정확히 일치합니다.

---

### 2. 레이아웃과 배치 (Figma Auto Layout $\rightarrow$ CSS Flexbox / Grid)

피그마의 핵심 기능인 오토 레이아웃(Auto Layout)은 현대 웹 디자인의 표준 레이아웃 방식인 **CSS Flexbox**와 같은 원리로 작동합니다.

| 피그마 (Auto Layout 속성) | HTML / CSS (Flexbox) 속성 | 설명 |
| --- | --- | --- |
| **Direction (가로/세로 방향)** | `flex-direction: row / column` | 요소들이 정렬되는 주축 방향 |
| **Spacing (간격)** | `gap: Opx` | 자식 요소들 사이의 여백 |
| **Padding (내부 여백)** | `padding: Opx` | 부모 박스 안쪽의 여백 |
| **Alignment (정렬)** | `justify-content`, `align-items` | 내부 요소들의 수평/수직 정렬 위치 |
| **Space between (양쪽 끝 정렬)** | `justify-content: space-between` | 요소를 양 끝으로 밀어내기 |

#### 크기 조절 방식 (Resizing)

* **Fixed (고정)**: `width: Opx`, `height: Opx` (고정된 크기)
* **Hug (내용에 맞춤)**: `width: fit-content` (내용물의 크기에 따라 박스 크기 자동 조절)
* **Fill (채우기)**: `flex: 1` 또는 `width: 100%` (부모의 남은 공간을 가득 채우기)

---

### 3. 스타일과 디자인 속성 (Figma Properties $\rightarrow$ CSS Properties)

피그마 우측 패널(Design 패널)의 시각적 속성들은 그대로 CSS 코드로 작성됩니다.

* **Fill (배경 색상 및 그라데이션)**
* 단색: `background-color: #HEXCODE;`
* 그라데이션: `background: linear-gradient(...);`


* **Stroke (테두리)**
* `border: [두께] [종류] [색상];` (예: `border: 1px solid #e5e5e5;`)


* **Corner Radius (모서리 둥글기)**
* `border-radius: Opx;`


* **Effects (그림자 및 블러)**
* Drop Shadow: `box-shadow: X축 Y축 블러 퍼짐 색상;`
* Layer Blur: `filter: blur(Opx);`


* **Opacity (투명도)**
* `opacity: 0.5;` 또는 `rgba()`


* **Typography (텍스트 스타일)**
* 글꼴: `font-family`
* 크기: `font-size`
* 두께: `font-weight`
* 행간: `line-height`
* 자간: `letter-spacing`



---

### 요약

* **HTML**은 웹페이지의 내용과 뼈대(구조)를 담당하며, 피그마의 **프레임, 텍스트, 이미지 레이어**가 이에 해당합니다.
* **CSS**는 웹페이지의 모양새와 배치(스타일 및 레이아웃)를 담당하며, 피그마의 **오토 레이아웃, 컬러, 그림자, 폰트 설정 등 우측 패널의 모든 디자인 속성**이 이에 해당합니다.
