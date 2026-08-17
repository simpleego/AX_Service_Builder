# Figma 컴포넌트 설계 원칙

> Figma 공식 Help Center의 **Components, Variants, Component Properties, Auto Layout, Variables, Libraries 관련 최신 문서**를 기준으로 정리하면, 좋은 컴포넌트 설계는 단순히 여러 화면에서 재사용하는 수준을 넘어 **UI의 규칙과 변경 가능한 범위를 체계적으로 정의하는 것**이라고 볼 수 있습니다. Figma에서 Main Component가 기준을 정의하고 Instance가 이를 재사용하며, Main Component의 변경 사항을 Instance에 전달하는 구조가 기본입니다. ([Figma Help Center][1])

---

## 1. 컴포넌트는 반복되는 UI를 기준으로 만든다

모든 요소를 컴포넌트로 만드는 것보다 **반복해서 사용되거나 일관성이 필요한 UI 요소**를 컴포넌트로 만드는 것이 중요합니다.

대표적인 대상은 Button, Input, Checkbox, Card, Navigation, Modal, List Item 등입니다. Figma는 컴포넌트를 재사용 가능한 디자인 요소로 정의하며, 작은 UI 요소뿐 아니라 메뉴나 레이아웃 같은 복합 요소도 컴포넌트로 구성할 수 있습니다. ([Figma Help Center][1])

```text
UI
│
├── Button
├── Input
├── Checkbox
├── Card
│   ├── Image
│   ├── Title
│   └── Button
│
└── Navigation
```

따라서 기본 원칙은 다음과 같이 이해할 수 있습니다.

> **반복되는 UI → Component
> 변경 가능한 부분 → Property
> 상태 차이 → Variant**

---

## 2. 컴포넌트 이름은 "모양"보다 "역할"을 표현한다

예를 들어 다음 이름은 권장하기 어렵습니다.

```text
BlueButton
BigBlueButton
GrayButton
Rectangle01
Frame123
```

색상이나 크기는 나중에 변경될 수 있기 때문입니다.

대신 UI가 수행하는 **의미와 역할**을 기준으로 이름을 정의합니다.

```text
Button
Button/Primary
Button/Secondary

Input
Input/Search
Input/Password
```

Figma 역시 `blue-large-button`처럼 현재의 시각적 형태를 이름으로 사용하는 것보다 컴포넌트가 **무엇인지**를 나타내는 이름을 권장합니다. 또한 `/`를 이용한 계층적 네이밍을 지원합니다. ([Figma Help Center][2])

예:

```text
Button/Primary/Default
Button/Primary/Hover
Button/Secondary/Default
Button/Secondary/Hover
```

다만 Variants를 사용하는 경우에는 아래처럼 더 단순하게 만들 수 있습니다.

```text
Component : Button

Properties
 ├─ Type
 ├─ State
 └─ Size
```

---

## 3. 상태 차이는 Variant로 관리한다

버튼 하나를 다음과 같이 별개의 컴포넌트로 만드는 방식은 관리하기 어렵습니다.

```text
PrimaryButton
PrimaryButtonHover
PrimaryButtonPressed
PrimaryButtonDisabled
SecondaryButton
SecondaryButtonHover
...
```

Variant를 사용하면 하나의 `Button` Component Set에서 속성으로 관리할 수 있습니다. Figma의 Variant Property는 `state`, `color`, `size`와 같은 컴포넌트의 차이를 속성으로 표현하기 위한 기능입니다. ([Figma Help Center][3])

예를 들어:

```text
Button

Type
 ├─ Primary
 ├─ Secondary
 └─ Tertiary

State
 ├─ Default
 ├─ Hover
 ├─ Pressed
 └─ Disabled

Size
 ├─ Small
 ├─ Medium
 └─ Large
```

프론트엔드 코드로 생각하면 다음과 상당히 유사합니다.

```jsx
<Button
    type="primary"
    state="default"
    size="medium"
/>
```

즉 Figma의 Variant는 **디자인을 프로그래밍 구조에 가까운 형태로 표현하는 기능**이라고 이해할 수 있습니다. Figma도 Variant 속성을 코드 컴포넌트와 연결할 수 있다고 설명합니다. ([Figma Help Center][3])

---

## 4. Variant를 지나치게 많이 만들지 않는다

Variant는 단순히 가능한 모든 경우의 수를 만드는 기능이 아닙니다.

예를 들어:

```text
Type  : 3개
State : 4개
Size  : 3개
Icon  : 2개
```

모든 조합을 Variant로 만들면

```text
3 × 4 × 3 × 2 = 72 Variants
```

가 필요할 수 있습니다.

이런 구조보다 **시각적·구조적 상태 변화는 Variant**, 단순한 내용 변경은 Component Property로 분리하는 것이 관리하기 좋습니다. Figma 역시 Component Properties와 Variants를 이용해 사용자가 실제로 변경해야 하는 부분만 적절한 컨트롤로 노출하도록 권장합니다. ([Figma Help Center][4])

---

# 5. 변경 가능한 부분은 Component Property로 만든다

Figma Component Property는 컴포넌트 Instance에서 변경할 수 있는 부분을 명시적으로 정의합니다. 대표적으로 Variant, Text, Boolean, Instance Swap 등의 방식이 사용됩니다. ([Figma Help Center][5])

버튼이라면 다음처럼 설계할 수 있습니다.

| 변경 대상                      | Figma 설계         |
| -------------------------- | ---------------- |
| Primary / Secondary        | Variant          |
| Default / Hover / Disabled | Variant          |
| Small / Medium / Large     | Variant          |
| 버튼 글자                      | Text Property    |
| 아이콘 표시 여부                  | Boolean Property |
| 어떤 아이콘을 사용할지               | Instance Swap    |

따라서:

```text
Button
│
├─ Type      = Primary
├─ State     = Default
├─ Size      = Medium
├─ Label     = "로그인"
├─ ShowIcon  = True
└─ Icon      = LoginIcon
```

처럼 하나의 컴포넌트가 다양한 상황을 처리할 수 있습니다.

---

# 6. 레이아웃은 Auto Layout을 기본으로 설계한다

실무에서 가장 중요한 원칙 가운데 하나입니다.

다음과 같은 버튼을 생각할 수 있습니다.

```text
┌─────────────────────┐
│  🔍   검색하기      │
└─────────────────────┘
```

텍스트가

```text
검색
```

에서

```text
상품 상세 검색하기
```

로 변경되어도 버튼 크기가 자연스럽게 바뀌어야 합니다.

Auto Layout은 콘텐츠가 추가·삭제·변경되거나 크기가 바뀔 때 레이아웃이 자동으로 조정되도록 합니다. Figma는 Auto Layout에서 방향, Padding, Gap, Alignment와 함께 `Hug contents`, `Fill container`, `Fixed` 등의 크기 조정 방식을 제공합니다. ([Figma Help Center][6])

웹 개발과 대응시키면 개념적으로:

```text
Figma              CSS

Auto Layout   ↔    Flexbox
Gap           ↔    gap
Padding       ↔    padding
Fill          ↔    flex-grow / width
Hug Contents  ↔    content 기반 크기
```

에 가깝습니다. 최근 Figma 문서에서도 Auto Layout을 CSS Flexbox와 연계해 설명하고 있습니다. ([Figma Help Center][7])

---

# 7. 작은 컴포넌트를 조합하여 복잡한 컴포넌트를 만든다

큰 UI 하나를 처음부터 하나의 거대한 컴포넌트로 만드는 것보다 작은 컴포넌트를 조합하는 **모듈형 구조**가 유지보수에 유리합니다.

예를 들어 Card를 다음처럼 구성할 수 있습니다.

```text
ProductCard
│
├── ProductImage
│
├── ProductInfo
│   ├── ProductName
│   ├── Price
│   └── Rating
│
└── Button
```

Button이나 Rating이 변경되면 이를 포함하는 여러 Card에서도 변경 사항을 일관되게 관리할 수 있습니다.

Figma는 이를 **Nested Instance** 구조로 지원하며, 복잡한 컴포넌트를 작은 컴포넌트 조합으로 구성하면 일관성과 유지보수성이 높아진다고 설명합니다. ([Figma Help Center][8])

개발 관점에서도:

```jsx
<ProductCard>
    <ProductImage />
    <ProductInfo />
    <Button />
</ProductCard>
```

와 유사한 구조가 됩니다.

---

# 8. 색상·간격·크기는 직접 값보다 Variables를 사용한다

예를 들어 버튼의 색상을 모든 컴포넌트에 직접

```text
#2563EB
```

로 지정하기보다:

```text
color.primary
color.surface
color.text.primary
color.error
```

와 같이 의미 기반 Variable을 사용하는 것이 좋습니다.

Figma Variables는 Color, Number, String 등의 값을 재사용하고 Light/Dark 또는 Mobile/Desktop 같은 Context에 따라 값을 변경할 수 있도록 설계되어 있습니다. 또한 Design Token을 구현하는 핵심 도구로 사용됩니다. ([Figma Help Center][9])

예:

```text
Primitive

blue.500
   ↓

Semantic

color.primary
   ↓

Component

button.background.primary
```

Dark Mode에서는:

```text
color.surface

Light → #FFFFFF
Dark  → #121212
```

처럼 동일한 의미의 토큰에 서로 다른 Mode 값을 적용할 수 있습니다. ([Figma Help Center][10])

---

# 9. Instance를 가능하면 Detach하지 않는다

Component를 사용하는 목적은 **Main Component와 Instance의 관계를 유지하는 것**입니다.

```text
Main Component
      │
      ├────────────┐
      ↓            ↓
Instance A     Instance B
      ↓            ↓
Screen A       Screen B
```

Main Component가 변경되면 연결된 Instance가 해당 업데이트를 전달받을 수 있습니다. ([Figma Help Center][1])

따라서 Instance를 계속 Detach해야 하는 상황이라면 보통 다음과 같은 설계 문제를 의심할 수 있습니다.

```text
Property가 부족함
      ↓
Variant 구조가 부족함
      ↓
Nested Component가 필요함
      ↓
컴포넌트 자체가 지나치게 경직됨
```

최근 Figma에서는 이러한 유연성을 높이기 위해 **Slots**도 제공하며, Card·Modal·List와 같이 내부 콘텐츠 구성이 다양한 컴포넌트에서 Instance를 분리하지 않고 내용을 추가·정렬할 수 있도록 지원합니다. ([Figma Help Center][11])

---

# 10. 컴포넌트 자체에 사용 규칙을 포함한다

디자인 시스템의 규모가 커질수록 단순히 컴포넌트를 만들어 놓는 것보다 다음과 같은 정보가 중요해집니다.

```text
Button / Primary

사용 목적
  주요 행동을 실행할 때 사용

사용 예
  결제하기
  회원가입
  저장

주의
  한 화면에서 Primary Button을
  지나치게 여러 개 사용하지 않음
```

Figma는 Components, Styles, Variables에 의미 있는 이름을 사용하고 간단한 Description과 외부 문서 링크 등을 추가하는 방식을 디자인 시스템 문서화 방법으로 안내합니다. ([Figma Help Center][12])

---

# Figma 컴포넌트 설계 핵심 원칙 정리

| 원칙                        | 핵심 내용                     |
| ------------------------- | ------------------------- |
| **1. 재사용성**               | 반복되는 UI를 Component로 만든다   |
| **2. 의미 있는 이름**           | 모양보다 역할을 기준으로 명명한다        |
| **3. Variant**            | 상태·크기·종류 차이를 구조화한다        |
| **4. Component Property** | 변경 가능한 부분만 사용자에게 노출한다     |
| **5. Auto Layout**        | 콘텐츠 변화에 반응하는 구조를 만든다      |
| **6. Modular Design**     | 작은 Component를 조합한다        |
| **7. Variables**          | 색상·Spacing·Size를 Token화한다 |
| **8. Instance 유지**        | 불필요한 Detach를 피한다          |
| **9. Nested Components**  | 복잡한 UI를 작은 컴포넌트 조합으로 구성한다 |
| **10. Documentation**     | 사용 목적과 규칙을 함께 관리한다        |

---

## 최종적으로 권장되는 구조

예를 들어 **Button Component**는 다음 정도의 구조라면 상당히 잘 설계된 형태입니다.

```text
Button
│
├── Auto Layout
│     ├── Horizontal
│     ├── Gap = spacing.2
│     └── Padding = spacing.3 / spacing.4
│
├── Properties
│     ├── Type
│     │     ├── Primary
│     │     └── Secondary
│     │
│     ├── State
│     │     ├── Default
│     │     ├── Hover
│     │     ├── Pressed
│     │     └── Disabled
│     │
│     ├── Size
│     │     ├── Small
│     │     ├── Medium
│     │     └── Large
│     │
│     ├── Label : Text Property
│     ├── ShowIcon : Boolean
│     └── Icon : Instance Swap
│
└── Variables
      ├── color.primary
      ├── color.on-primary
      ├── spacing.2
      ├── spacing.3
      └── radius.medium
```

이를 개발 코드 관점으로 바꾸면:

```jsx
<Button
    type="primary"
    state="default"
    size="medium"
    icon="search"
>
    검색하기
</Button>
```

와 거의 동일한 사고방식이 됩니다.

따라서 비전공자가 Figma 컴포넌트를 학습할 때는 **“도형을 Component로 바꾸는 조작법”보다 `재사용 → 상태 → 속성 → 레이아웃 → 토큰 → 조합`의 순서로 이해하는 것이 더 중요합니다.** Figma 공식 자료도 재사용 가능한 블록, 의미 있는 이름, Auto Layout, Component Properties/Variants, Variables, 문서화를 디자인 시스템의 핵심 패턴으로 제시하고 있습니다. ([Figma Help Center][13])

[1]: https://help.figma.com/hc/en-us/articles/360038662654-Guide-to-components-in-Figma?utm_source=chatgpt.com "Guide to components in Figma"
[2]: https://help.figma.com/hc/en-us/articles/360038663994-Name-and-organize-components?utm_source=chatgpt.com "Name and organize components"
[3]: https://help.figma.com/hc/en-us/articles/360056440594-Create-and-use-variants?utm_source=chatgpt.com "Create and use variants"
[4]: https://help.figma.com/hc/en-us/articles/39747637290263-Components-collection-Tips-for-component-management?utm_source=chatgpt.com "Tips for component management"
[5]: https://help.figma.com/hc/en-us/articles/5579474826519-Explore-component-properties?utm_source=chatgpt.com "Explore component properties"
[6]: https://help.figma.com/hc/en-us/articles/360040451373-Guide-to-auto-layout?utm_source=chatgpt.com "Guide to auto layout"
[7]: https://help.figma.com/hc/en-us/articles/42031586813719-Use-auto-layout-with-CSS-Flexbox-in-mind?utm_source=chatgpt.com "Use auto layout with CSS Flexbox in mind"
[8]: https://help.figma.com/hc/en-us/articles/39723486706455-Components-collection-Nesting-instances-fundamentals?utm_source=chatgpt.com "Components collection: Nesting instances fundamentals"
[9]: https://help.figma.com/hc/en-us/articles/15339657135383-Guide-to-variables-in-Figma?utm_source=chatgpt.com "Guide to variables in Figma"
[10]: https://help.figma.com/hc/en-us/articles/18490793776023-Update-1-Tokens-variables-and-styles?utm_source=chatgpt.com "Update 1: Tokens, variables, and styles"
[11]: https://help.figma.com/hc/en-us/articles/38231200344599-Use-slots-to-build-flexible-components-in-Figma?utm_source=chatgpt.com "Use slots to build flexible components in Figma"
[12]: https://help.figma.com/hc/en-us/articles/7938814091287-Add-descriptions-to-styles-components-and-variables?utm_source=chatgpt.com "Add descriptions to styles, components, and variables"
[13]: https://help.figma.com/hc/en-us/articles/38978644498199-AI-workflows-collection-Best-practices-to-help-Figma-AI-understand-your-design-system?utm_source=chatgpt.com "Best practices to help Figma AI understand your design ..."
