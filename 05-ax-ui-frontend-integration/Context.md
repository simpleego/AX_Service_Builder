# 컴포넌트를 Provider로 감싸는 문법

Provider로 감싸는 기본 문법은 다음과 같습니다.

```jsx
<컨텍스트이름.Provider value={공급할값}>
    {/* 값을 사용할 하위 컴포넌트들 */}
</컨텍스트이름.Provider>
```

## 단계별 예시

**1. Context 만들기** (`src/chapter_14/ThemeContext.jsx`)

```jsx
import React from "react";
const ThemeContext = React.createContext();   // 기본값을 넣으려면 createContext("light")
export default ThemeContext;
```

**2. Provider로 감싸기** (`src/chapter_14/DarkOrLight.jsx`)

```jsx
import ThemeContext from "./ThemeContext";

<ThemeContext.Provider value={{ theme, toggleTheme }}>
    <MainContent />
</ThemeContext.Provider>
```

**3. 하위에서 꺼내 쓰기** (`src/chapter_14/MainContent.jsx`)

```jsx
const { theme, toggleTheme } = useContext(ThemeContext);
```

## 문법 포인트

- **`.Provider`**: Context 객체에 붙어 있는 컴포넌트입니다. 따로 만들 필요가 없습니다.
- **`value` 속성은 필수**이고, 이름도 반드시 `value`여야 합니다.
- **중괄호 두 겹 `{{ }}`**: 바깥 `{}`는 JSX에서 JS 표현식을 쓰겠다는 뜻이고, 안쪽 `{}`는 객체입니다. 값이 하나면 `value={theme}`처럼 한 겹으로 씁니다.
- **여러 컴포넌트 감싸기** 가능:

  ```jsx
  <ThemeContext.Provider value={theme}>
      <Header />
      <MainContent />
      <Footer />
  </ThemeContext.Provider>
  ```

## 여러 Context를 함께 쓸 때 (중첩)

```jsx
<ThemeContext.Provider value={theme}>
    <UserContext.Provider value={user}>
        <MainContent />
    </UserContext.Provider>
</ThemeContext.Provider>
```

## 참고: React 19의 새 문법

React 19부터는 `.Provider`를 생략할 수 있습니다.

```jsx
<ThemeContext value={{ theme, toggleTheme }}>
    <MainContent />
</ThemeContext>
```

React 18 프로젝트에서는 `ThemeContext.Provider` 형태를 써야 합니다.
