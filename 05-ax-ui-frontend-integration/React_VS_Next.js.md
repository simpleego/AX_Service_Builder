# React VS Next.js

> **React는 UI를 만드는 라이브러리이고, Next.js는 React를 기반으로 웹 애플리케이션 전체를 만들기 위한 프레임워크**입니다.

| 구분 | React | Next.js |
|---|---|---|
| 성격 | UI 라이브러리 | React 기반 프레임워크 |
| 주요 역할 | 화면 구성 | 화면 + 라우팅 + 서버 기능 + 배포 구조 |
| 라우팅 | 별도 라이브러리 필요 | 기본 제공 |
| 서버 렌더링 | 직접 구성 필요 | SSR/SSG 지원 |
| API 서버 | 별도 백엔드 필요 | API/서버 기능 일부 구현 가능 |
| SEO | 추가 설정 필요 | 상대적으로 유리 |
| 프로젝트 구조 | 자유로움 | 정해진 구조가 있음 |

[React 기초](https://jeonwon.dev/web/nextjs/nextjs-summary/#nextjs-%EA%B8%B0%EB%B3%B8-%EA%B5%AC%EC%A1%B0)

---
<img width="1280" height="720" alt="image" src="https://github.com/user-attachments/assets/006fbf3c-4028-43f5-a9b1-30bdd880903b" />

---




예를 들어 React만 사용하면 보통:

```text
React
 + React Router
 + FastAPI
 + 별도 SEO 설정
 + 별도 서버 구성
```

처럼 필요한 기능을 조합합니다.

Next.js를 사용하면:

```text
Next.js
 ├─ React
 ├─ Routing
 ├─ Server Rendering
 ├─ API
 └─ Build/Deployment 구조
```

가 상당 부분 포함되어 있습니다.

특히 중요한 차이는 렌더링 방식입니다.

React를 일반적으로 사용하면:

```text
브라우저
   ↓
JavaScript 실행
   ↓
화면 생성
```

즉 CSR(Client Side Rendering)이 중심입니다.

Next.js는 다음과 같은 방식도 쉽게 사용할 수 있습니다.

```text
서버
 ↓
HTML 생성
 ↓
브라우저로 전달
```

즉 SSR(Server Side Rendering)을 지원합니다.

비유하면:

> **React = 엔진**
>
> **Next.js = React 엔진이 들어간 완성된 자동차**

라고 설명하면 이해하기 쉽습니다.

AX 풀스택 과정 관점에서는 **React를 먼저 이해한 뒤 Next.js로 넘어가는 순서**가 좋습니다. React의 컴포넌트, props, state, hook 개념을 알아야 Next.js도 제대로 이해할 수 있습니다.
