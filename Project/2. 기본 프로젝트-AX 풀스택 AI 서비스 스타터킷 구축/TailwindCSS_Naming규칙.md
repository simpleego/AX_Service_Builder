# Tailwind CSS의 Naming 규칙

Tailwind CSS의 유틸리티 클래스는 직관적인 명명 규칙(Naming Convention)을 기반으로 CSS 속성과 값을 조합하여 구성됩니다. 주요 네이밍 규칙과 실무에서 자주 사용되는 핵심 유틸리티 클래스를 정리해 드립니다.

---

<img width="1122" height="1402" alt="image" src="https://github.com/user-attachments/assets/cc6c5747-8e63-4d41-8446-6e523f77aa9b" />

---

## 1. Tailwind CSS 네이밍 규칙 (Naming Rules)

Tailwind는 기본적으로 `[속성]-[값]` 형태의 일관되고 직관적인 패턴을 따릅니다.

* **기본 패턴 (`property-value`):** CSS 속성 축약어 또는 이름을 먼저 쓰고, 뒤에 스케일 값을 붙입니다.
* 예: `text-lg` (`font-size: 1.125rem`), `bg-blue-500` (`background-color: #3b82f6`)


* **간격 시스템 (Spacing Scale):** 기본 단위는 `1`당 `0.25rem`(4px)입니다.
* 예: `p-4` = `padding: 1rem` (16px), `m-2` = `margin: 0.5rem` (8px)
* 방향 축약: `pt-` (top), `pb-` (bottom), `pl-` (left), `pr-` (right), `px-` (left & right), `py-` (top & bottom)


* **반응형 디자인 (Responsive Prefixes):** 화면 크기(Breakpoints)별 접두사를 붙여 분기 처리를 합니다.
* `sm:` (640px 이상), `md:` (768px 이상), `lg:` (1024px 이상), `xl:` (1280px 이상)
* 예: `md:flex` (화면 너비 768px 이상에서 `display: flex` 적용)


* **상태 변형 (State Modifiers):** 마우스 오버, 포커스 등 특정 상태를 지정합니다.
* `hover:`, `focus:`, `active:`, `disabled:`
* 예: `hover:bg-blue-600`


* **임의 값 사용 (Arbitrary Values):** 정의된 스케일에 없는 고유 값이 필요할 때 대괄호(`[]`)를 사용합니다.
* 예: `w-[320px]`, `bg-[#1da1f2]`, `top-[117px]`



---

## 2. 자주 사용되는 주요 CSS 유틸리티 클래스 표

| 카테고리 | 유틸리티 클래스 | CSS 대응 속성 | 설명 |
| --- | --- | --- | --- |
| **Layout / Display** | `flex` / `grid` | `display: flex / grid` | 플렉스박스 및 그리드 레이아웃 설정 |
|  | `hidden` | `display: none` | 요소 숨기기 |
|  | `block` / `inline-block` | `display: block / inline-block` | 블록 및 인라인 블록 표시 |
| **Flexbox Alignment** | `items-center` | `align-items: center` | 교차 축 기준 수직 정렬 |
|  | `justify-center` | `justify-content: center` | 주 축 기준 중앙 정렬 |
|  | `justify-between` | `justify-content: space-between` | 양 끝 정렬 (Space between) |
| **Spacing (Padding/Margin)** | `p-4` / `m-4` | `padding/margin: 1rem (16px)` | 사방 여백 적용 |
|  | `px-6` / `py-3` | 수평(좌우) / 수직(상하) 축 개별 여백 | 축별 여백 제어 |
|  | `space-x-4` | 자식 요소 간 수평 마진 부여 | Flex/Grid 자식 간 간격 설정 |
| **Typography** | `text-sm` / `text-lg` | `font-size` 조절 | 폰트 크기 변경 |
|  | `font-bold` / `font-medium` | `font-weight: 700 / 500` | 폰트 굵기 조절 |
|  | `text-center` / `text-left` | `text-align: center / left` | 텍스트 정렬 |
| **Colors** | `bg-white` / `bg-slate-100` | `background-color` | 배경색 설정 |
|  | `text-blue-600` / `text-gray-900` | `color` | 텍스트 색상 설정 |
| **Sizing** | `w-full` / `w-auto` | `width: 100% / auto` | 가로 크기 설정 |
|  | `h-screen` / `h-full` | `height: 100vh / 100%` | 세로 크기 설정 |
| **Borders & Effects** | `rounded-md` / `rounded-full` | `border-radius` | 모서리 둥글게 처리 |
|  | `border` / `border-gray-200` | 테두리 두께 및 색상 설정 | 박스 테두리 생성 |
|  | `shadow-md` / `shadow-lg` | `box-shadow` | 그림자 효과 적용 |


