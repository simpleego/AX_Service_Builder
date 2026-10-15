# 5-4. CSS 프레임워크 기반 스타일링 — 8H

[전체 목차](00-index.md) · [이전: 상태 관리](05-03-state.md) · [다음: API 연동](05-05-api.md)

## 단원 목차

- [1. 목표와 시간표](#s1)
- [2. React에서 스타일을 다루는 방법](#s2)
- [3. Tailwind CSS v4 설치](#s3)
- [4. 유틸리티 클래스 읽고 쓰기](#s4)
- [5. 디자인 토큰: 시안을 테마로](#s5)
- [6. 스타일 컴포넌트: UI 키트 만들기](#s6)
- [7. 회원 화면에 적용](#s7)
- [8. 실습과 확인 문제](#s8)
- [9. 강사 노트](#s9)

<a id="s1"></a>
## 1. 목표와 시간표

CSS 프레임워크를 프로젝트에 설치하고, 디자인 시안의 색·글꼴·간격을 토큰으로 옮긴다. 반복되는 스타일을 Button·Input·Modal 같은 공통 컴포넌트로 감싸 화면 전체를 일관되게 만든다.

| 교시 | 내용 | 활동 |
|---|---|---|
| 1 | 스타일 방식 비교: CSS·Modules·CSS-in-JS·Tailwind | 같은 버튼을 네 방식으로 읽기 |
| 2 | Tailwind v4 설치, 유틸리티 문법, 상태 변형 | 라이브 코딩: 카드 꾸미기 |
| 3 | 디자인 토큰(@theme), 공통 컴포넌트 설계 | 피그마 시안에서 토큰 뽑기 |
| 4 | Button(variant)·Input(label·오류) 제작 | 페어 제작 |
| 5 | Modal·StatusMessage·Toast 스타일 | 접근성 속성 확인 |
| 6 | 회원 목록·폼·로그인 화면 적용 | 기존 마크업 교체 |
| 7 | 디자인 리뷰 기준으로 다듬기 | 간격·대비·포커스 점검 |
| 8 | 검토·평가 | 화면 캡처 갤러리 리뷰, 배움일기 |

<a id="s2"></a>
## 2. React에서 스타일을 다루는 방법

| 방식 | 예 | 장점 | 단점 |
|---|---|---|---|
| 전역 CSS | `import "./App.css"` | 익숙함 | 클래스 이름 충돌 |
| CSS Modules | `styles.button` | 파일 단위로 이름 격리 | 파일 왕복, 공통 값 관리 별도 |
| CSS-in-JS | styled-components | JS 값으로 스타일 분기 | 런타임 비용, 서버 컴포넌트와 궁합 문제 |
| 유틸리티 CSS | Tailwind | 파일 왕복 없음, 토큰 강제, 빌드 시 미사용 제거 | 클래스가 길어짐 → 컴포넌트로 감싸 해결 |

```jsx
// styled-components 방식 (비교용, 이번 과정에서는 설치하지 않음)
const Button = styled.button`
  padding: 8px 16px;
  background: ${(props) => (props.$danger ? "#dc2626" : "#4f46e5")};
`;

// Tailwind 방식 (이번 과정에서 사용)
<button className="rounded-lg bg-brand-600 px-4 py-2 text-white">저장</button>
```

이번 과정은 Tailwind를 쓴다. 현업 채용 공고 빈도가 높고, 클래스가 디자인 토큰에서만 나오므로 **AI가 생성한 코드도 같은 색·간격 체계를 따르게 만들기 쉽다.**

<a id="s3"></a>
## 3. Tailwind CSS v4 설치

```powershell
npm install tailwindcss @tailwindcss/vite
```

`vite.config.js`

```js
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
});
```

`src/index.css` — 기존 내용을 지우고 한 줄로 시작한다.

```css
@import "tailwindcss";
```

> v3 자료와의 차이: v4는 `tailwind.config.js`와 `@tailwind base;` 세 줄이 필요 없다. 인터넷·AI가 v3 방식 코드를 주는 경우가 많으므로 **버전을 확인**하는 습관을 들인다. VS Code 확장 "Tailwind CSS IntelliSense"를 설치하면 자동완성과 실제 CSS 미리보기가 된다.

<a id="s4"></a>
## 4. 유틸리티 클래스 읽고 쓰기

| 분류 | 클래스 예 | 뜻 |
|---|---|---|
| 간격 | `p-4`, `px-3`, `mt-6`, `gap-2`, `space-y-4` | 4 = 1rem(16px), 단위 0.25rem |
| 크기 | `w-full`, `max-w-lg`, `min-h-dvh` | 너비·높이 |
| 레이아웃 | `flex`, `grid`, `items-center`, `justify-between` | 배치 |
| 글자 | `text-sm`, `font-semibold`, `text-slate-500`, `truncate` | 크기·굵기·색·말줄임 |
| 테두리 | `rounded-lg`, `border`, `border-slate-200` | 모서리·선 |
| 배경·그림자 | `bg-white`, `bg-slate-900/40`, `shadow-sm` | `/40` = 투명도 40% |

**상태 변형(variant)** — 접두사로 조건을 붙인다.

| 접두사 | 적용 조건 | 예 |
|---|---|---|
| `hover:` | 마우스 올림 | `hover:bg-brand-700` |
| `focus-visible:` | 키보드 포커스 | `focus-visible:outline-2` |
| `disabled:` | 비활성 | `disabled:opacity-50` |
| `aria-invalid:` | `aria-invalid="true"` | `aria-invalid:border-red-500` |
| `sm:` `md:` `lg:` | 화면 너비 이상 | 6일차에 집중 |

> 접근성 원칙: `outline-none`으로 포커스 표시를 지우면 키보드 사용자가 위치를 잃는다. 지웠다면 반드시 `focus-visible:` 또는 `focus:ring-*`으로 대체한다.

<a id="s5"></a>
## 5. 디자인 토큰: 시안을 테마로

피그마 시안에서 **브랜드 색, 글꼴**을 뽑아 `@theme`에 등록하면 `bg-brand-600`, `text-brand-700` 같은 클래스가 생긴다. 시안의 색을 화면마다 `#4f46e5`로 직접 쓰지 않는다.

`src/index.css` (완성 예제와 같음)

```css
@import "tailwindcss";

@theme {
  --color-brand-50: oklch(0.97 0.02 260);
  --color-brand-600: oklch(0.55 0.2 260);
  --color-brand-700: oklch(0.48 0.2 260);
  --font-sans: "Pretendard", system-ui, sans-serif;
}
```

| 시안 항목 | 토큰 | 사용 예 |
|---|---|---|
| Primary | `--color-brand-600` | 주 버튼 배경 |
| Primary Hover | `--color-brand-700` | 버튼 hover, 선택된 메뉴 글자 |
| Primary Light | `--color-brand-50` | 선택된 메뉴 배경 |
| 본문 글꼴 | `--font-sans` | 전체 기본 글꼴 |
| 회색·빨강·초록 | Tailwind 기본 `slate`, `red`, `emerald` | 본문, 위험, 성공 |

- Pretendard 글꼴을 실제로 쓰려면 `index.html`에 웹폰트 링크를 추가한다. 없으면 `system-ui`로 대체된다.
- 글자와 배경의 명도 대비는 **4.5:1 이상**(WCAG AA)을 맞춘다. 피그마 플러그인이나 브라우저 DevTools의 대비 검사를 쓴다.

<a id="s6"></a>
## 6. 스타일 컴포넌트: UI 키트 만들기

긴 클래스 문자열을 화면마다 복사하면 하나를 고칠 때 전부 고쳐야 한다. **스타일과 접근성 규칙을 컴포넌트 안에 가두고**, 화면에서는 의미만 고른다.

`src/components/ui/Button.jsx`

```jsx
const variants = {
  primary: "bg-brand-600 text-white hover:bg-brand-700",
  secondary: "border border-slate-300 bg-white text-slate-700 hover:bg-slate-50",
  danger: "bg-red-600 text-white hover:bg-red-700",
};

export default function Button({ variant = "primary", type = "button", className = "", ...props }) {
  return (
    <button
      type={type}
      className={`inline-flex items-center justify-center rounded-lg px-4 py-2 text-sm font-medium transition focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-brand-600 disabled:cursor-not-allowed disabled:opacity-50 ${variants[variant]} ${className}`}
      {...props}
    />
  );
}
```

- `type="button"` 기본값: 폼 안의 버튼이 뜻하지 않게 제출되는 버그를 막는다.
- `...props`: `onClick`, `disabled`, `aria-*`를 그대로 전달한다.

`src/components/ui/Input.jsx` — label·오류 연결을 매번 직접 쓰지 않게 한다.

```jsx
import { useId } from "react";

export default function Input({ label, error, id, ...props }) {
  const autoId = useId();
  const inputId = id ?? autoId;
  const errorId = `${inputId}-error`;

  return (
    <div className="space-y-1">
      <label htmlFor={inputId} className="block text-sm font-medium text-slate-700">
        {label}
      </label>
      <input
        id={inputId}
        aria-invalid={Boolean(error)}
        aria-describedby={error ? errorId : undefined}
        className="w-full rounded-lg border border-slate-300 px-3 py-2 text-sm focus:border-brand-600 focus:ring-2 focus:ring-brand-600/20 focus:outline-none aria-invalid:border-red-500"
        {...props}
      />
      {error && <p id={errorId} className="text-xs text-red-600">{error}</p>}
    </div>
  );
}
```

`useId`는 같은 컴포넌트를 여러 번 써도 겹치지 않는 id를 만든다. 2일차 `Field`의 수동 id를 대체한다.

`src/components/ui/Modal.jsx`

```jsx
import { useEffect } from "react";

export default function Modal({ open, title, onClose, children }) {
  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [open, onClose]);

  if (!open) return null;
  return (
    <div className="fixed inset-0 z-40 flex items-end justify-center bg-slate-900/40 sm:items-center" onClick={onClose}>
      <div
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
        className="max-h-[90dvh] w-full max-w-lg overflow-y-auto rounded-t-2xl bg-white p-6 shadow-xl sm:rounded-2xl"
        onClick={(event) => event.stopPropagation()}
      >
        <h2 id="modal-title" className="mb-4 text-lg font-semibold text-slate-900">{title}</h2>
        {children}
      </div>
    </div>
  );
}
```

`src/components/ui/StatusMessage.jsx` — 로딩·빈 상태·오류를 같은 모양으로 보여 준다(5일차에 사용).

```jsx
export default function StatusMessage({ title, description, action }) {
  return (
    <div className="rounded-xl border border-dashed border-slate-300 px-6 py-12 text-center">
      <p className="font-medium text-slate-800">{title}</p>
      {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}
```

Toast에는 종류별 배경색만 매핑한다.

```jsx
const tones = { info: "bg-slate-800", success: "bg-emerald-600", error: "bg-red-600" };
// <p className={`rounded-lg px-4 py-3 text-sm text-white shadow-lg ${tones[toast.type]}`}>
```

> 왜 `variants` 객체인가: Tailwind는 **소스 코드에 완성된 문자열로 적힌 클래스만** CSS로 만든다. `` `bg-${color}-600` ``처럼 조립하면 해당 클래스가 빌드에 빠진다. AI가 자주 만드는 실수이므로 리뷰 항목에 추가한다.

<a id="s7"></a>
## 7. 회원 화면에 적용

| 화면 | 바꿀 것 |
|---|---|
| MemberForm | 2일차 `Field` → `Input`, 버튼 → `Button`, 입력 2열 그리드 `grid gap-4 sm:grid-cols-2` |
| MemberCard | `article`에 `rounded-xl border bg-white p-4`, 정보는 `dl`/`dt`/`dd` |
| 목록 상단 | 제목·회원 수(왼쪽) + 검색·추가 버튼(오른쪽) `flex justify-between` |
| 모달 | App의 조건부 폼을 `Modal`로 감싸기 |
| 로그인 | 가운데 정렬 카드 `grid min-h-dvh place-items-center` |

MemberForm 적용 후 (완성 예제와 같음, 핵심 부분)

```jsx
<form onSubmit={submit} noValidate className="space-y-4">
  <div className="grid gap-4 sm:grid-cols-2">
    <Input label="이름" name="name" value={form.name} onChange={change} error={errors.name} />
    <Input label="아이디" name="username" value={form.username} onChange={change} error={errors.username} />
    <Input label="이메일" name="email" type="email" value={form.email} onChange={change} error={errors.email} />
    <Input label="전화번호" name="phone" type="tel" value={form.phone} onChange={change} />
    <Input label="도시" name="city" value={form.address.city} onChange={change} />
    <Input label="회사" name="companyName" value={form.company.name} onChange={change} />
  </div>
  <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
    <Button variant="secondary" onClick={onCancel}>취소</Button>
    <Button type="submit" disabled={submitting}>{submitting ? "저장 중..." : "저장"}</Button>
  </div>
</form>
```

### 디자인 리뷰 기준

| 항목 | 기준 |
|---|---|
| 간격 | 4의 배수 클래스만 사용(`p-3`, `gap-4`), 임의 값(`p-[13px]`) 지양 |
| 색 | 토큰·기본 팔레트만, hex 직접 입력 없음 |
| 위계 | 페이지 제목 `text-2xl` > 섹션 `text-lg` > 본문 `text-sm` |
| 상호작용 | 모든 버튼에 hover·focus-visible·disabled 상태 |
| 대비 | 회색 글자는 `text-slate-500` 이상 진하게 |
| 일관성 | 같은 역할의 요소는 같은 컴포넌트 |

<a id="s8"></a>
## 8. 실습과 확인 문제

### 실습 (4~7교시)

| 단계 | 할 일 | 완료 기준 |
|---|---|---|
| 1 | Tailwind 설치, `@theme` 토큰 등록 | `bg-brand-600`이 적용됨 |
| 2 | Button(3 variant)·Input 제작 | 키보드 Tab으로 포커스 링 확인 |
| 3 | Modal·StatusMessage 제작, Toast 색 적용 | Esc·바깥 클릭으로 닫힘 |
| 4 | MemberForm·MemberCard·목록 상단·로그인 화면 교체 | 기존 기능 그대로 동작 |
| 5 | 디자인 리뷰 기준으로 자체 점검 | 위반 0개 |
| 도전 | AI에게 "우리 UI 키트만 써서 회원 상세 카드 만들어 줘"라고 요청 | 새 색·임의 값 없이 생성되는지 리뷰 |

### 확인 문제

1. `` className={`text-${color}-600`} ``이 동작하지 않는 이유는?
2. 공통 Button의 기본 `type`을 `"button"`으로 둔 이유는?
3. `outline-none`을 쓸 때 반드시 함께 해야 할 일은?
4. 디자인 토큰을 쓰면 시안의 브랜드 색이 바뀔 때 무엇이 쉬워지는가?
5. Tailwind v3 방식 설정 파일을 AI가 주었을 때 어떻게 알아보는가?

### 과제

- 데스크톱 화면 캡처 2장(목록, 수정 모달)을 README에 추가한다.
- 배움일기: UI 키트로 감싼 컴포넌트 하나와 그 이유.

<a id="s9"></a>
## 9. 강사 노트

| 증상 | 원인 |
|---|---|
| 클래스를 줬는데 스타일 없음 | `index.css` import 누락, vite 플러그인 누락, 동적 클래스 조립 |
| 기존 Vite 기본 스타일과 충돌 | 템플릿의 `App.css`·`index.css` 기본 내용 삭제 안 함 |
| 자동완성이 안 됨 | IntelliSense 확장 설치, VS Code 재시작 |
| 버튼이 폼을 제출함 | `type` 누락 (공통 Button으로 해결) |

- 디자인 감각보다 **규칙 준수**를 평가한다. "예쁜가"가 아니라 "토큰·컴포넌트를 일관되게 썼는가".
- 피그마 시안이 없는 반은 `D:\AX_FullStack_Builder\피그마` 폴더의 기존 자료나 Tailwind 기본 팔레트로 진행한다.
