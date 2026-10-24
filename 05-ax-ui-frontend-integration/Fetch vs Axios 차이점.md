# Fetch vs Axios 차이점

Fetch와 Axios는 모두 JavaScript에서 HTTP 요청을 보내고 서버의 응답을 받아오는 기술입니다.

예를 들어 React 프론트엔드에서 FastAPI 백엔드의 데이터를 조회하거나 등록할 때 사용합니다.

가장 큰 차이점은 다음과 같습니다.

- Fetch: JavaScript 실행 환경에서 기본 제공하는 HTTP 요청 API
- Axios: HTTP 통신을 더 편리하게 처리하도록 만든 외부 라이브러리

## 1. Fetch와 Axios 비교

| 비교 항목      | Fetch                 | Axios                |
| ---------- | --------------------- | -------------------- |
| 종류         | 표준 Web API            | 외부 라이브러리             |
| 설치         | 불필요                   | `npm install axios`  |
| HTTP 요청    | GET, POST 등 지원        | GET, POST 등 지원       |
| 비동기 처리     | Promise, async/await  | Promise, async/await |
| JSON 응답 변환 | `response.json()` 호출  | 일반적으로 자동 변환          |
| JSON 요청 전송 | `JSON.stringify()` 사용 | 객체를 자동 직렬화           |
| HTTP 오류 처리 | `response.ok` 확인      | 기본적으로 4xx, 5xx 오류 발생 |
| 타임아웃       | AbortSignal 등 활용      | `timeout` 옵션 제공      |
| 공통 URL 설정  | 별도 함수 구성              | `baseURL` 제공         |
| 요청·응답 가로채기 | 직접 구현                 | Interceptor 제공       |
| JWT 자동 첨부  | 직접 구현                 | Interceptor로 간편하게 구현 |
| 의존성        | 추가 의존성 없음             | 추가 패키지 필요            |

[image](https://www.google.com/s2/favicons?domain=https://developer.mozilla.org\&sz=32)

MDN

+3

## 2. HTTP 요청 과정

두 기술의 기본 통신 흐름은 동일합니다.

React

프론트엔드

HTTP 요청

JSON 응답

FastAPI

백엔드

Fetch 또는 Axios가 HTTP 요청과 응답을 처리

Fetch든 Axios든 서버 입장에서는 일반적인 HTTP 요청을 받는 것이므로, FastAPI 백엔드 코드를 변경할 필요가 없습니다.

## 3. GET 요청 코드 비교

예를 들어 FastAPI 서버에서 사용자 정보를 가져오는 경우입니다.

① Fetch 방식

```

async function getUsers() {
  const response = await fetch("http://localhost:8000/users");

  if (!response.ok) {
    throw new Error(`HTTP 오류: ${response.status}`);
  }

  const data = await response.json();
  console.log(data);
}
  
```

② Axios 방식

```

import axios from "axios";

async function getUsers() {
  const response = await axios.get("http://localhost:8000/users");

  console.log(response.data);
}
  
```

핵심 차이는 응답 처리입니다.

- Fetch는 `response.json()`으로 JSON 응답을 JavaScript 객체로 변환합니다.
- Axios는 일반적인 JSON 응답을 자동 변환하여 `response.data`로 제공합니다.

## 4. POST 요청 코드 비교

사용자 이름과 나이를 서버에 등록하는 예제입니다.

① Fetch 방식

```

const user = { name: "홍길동", age: 25 };

const response = await fetch("http://localhost:8000/users", {
  method: "POST",
  headers: {
    "Content-Type": "application/json"
  },
  body: JSON.stringify(user)
});

if (!response.ok) {
  throw new Error(`HTTP 오류: ${response.status}`);
}

const data = await response.json();
console.log(data);

```

② Axios 방식

```

import axios from "axios";

const user = { name: "홍길동", age: 25 };

const response = await axios.post(
  "http://localhost:8000/users",
  user
);

console.log(response.data);

```

Axios는 일반적인 객체를 JSON으로 변환하고 필요한 헤더도 처리하므로 코드가 간단해집니다.

## 5. 가장 중요한 차이: 오류 처리

HTTP 404 또는 500 오류가 발생했다고 가정하겠습니다.

Fetch는 서버가 오류 응답을 반환하더라도 자동으로 예외가 발생하지 않습니다.

```
const response = await fetch("/api/users");

if (!response.ok) {
  throw new Error("HTTP 요청 실패");
}
```

반면 Axios는 기본적으로 200번대 이외의 HTTP 상태 코드에 대해 Promise를 거부하므로 `catch`에서 처리할 수 있습니다.

```
try {
  const response = await axios.get("/api/users");
  console.log(response.data);
} catch (error) {
  console.log("요청 실패:", error.response?.status);
}
```

다만 네트워크 자체가 실패하거나 CORS 오류가 발생하면 Fetch도 예외가 발생합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developer.mozilla.org\&sz=32)

MDN

+1



## 6. JWT 인증에서는 Axios가 왜 편리할까?

JWT를 사용하는 웹 애플리케이션에서는 인증이 필요한 API를 호출할 때마다 헤더에 토큰을 첨부해야 합니다.

```
Authorization: Bearer <JWT>
```

Axios는 Interceptor(인터셉터) 기능을 제공하기 때문에 인증 토큰 첨부를 공통으로 처리할 수 있습니다.

```
import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000"
});

// 요청 인터셉터
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("accessToken");

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

// 각 API 호출
const users = await api.get("/users");
const products = await api.get("/products");
```

위 코드는 모든 API 요청에 필요한 JWT 토큰을 자동으로 첨부합니다. 단, 실제 서비스에서는 XSS 등 토큰 탈취 위험을 고려해 저장 방식을 선택해야 합니다.

Axios의 인터셉터는 응답에도 적용할 수 있으므로 `401 Unauthorized` 오류에 대한 공통 처리나 Refresh Token 재발급 로직을 구성할 때도 유용합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://github.com\&sz=32)

GitHub

+1



## 7. 어떤 기술을 선택하는 것이 좋을까?

| 개발 상황                   | 추천        |
| ----------------------- | --------- |
| JavaScript 기초 및 HTTP 학습 | Fetch     |
| 간단한 Todo 앱              | Fetch     |
| 외부 API 데이터 조회           | Fetch     |
| React + FastAPI 프로젝트    | 둘 다 적합    |
| JWT 인증을 사용하는 서비스        | Axios가 편리 |
| 공통 요청 설정이 많은 프로젝트       | Axios     |
| 외부 의존성을 최소화할 때          | Fetch     |

### 결론

Fetch는 HTTP 통신의 기본 원리를 배우기에 좋고, Axios는 반복적인 HTTP 요청 작업을 체계적으로 관리하는 데 유리합니다.

특히 React + FastAPI 기반의 프로젝트 교육이라면 다음 순서를 추천합니다.

1. Fetch로 GET, POST, PUT, DELETE 요청을 직접 구현합니다.
2. Fetch를 이용해 HTTP 상태 코드, JSON 변환, 예외 처리를 학습합니다.
3. 동일한 코드를 Axios로 변경하여 차이점을 확인합니다.
4. Axios의 `baseURL`, Interceptor를 활용하여 JWT 인증과 연동합니다.

중요한 점은 Axios가 Fetch보다 무조건 뛰어난 기술이 아니라, HTTP 통신을 편리하게 관리하기 위한 선택지라는 것입니다. 실제로 Fetch만으로도 대규모 웹 애플리케이션을 충분히 개발할 수 있습니다.

공식 문서: [MDN Fetch API](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch?utm_source=chatgpt.com) · [Axios 공식 문서](https://axios-http.com/kr/docs/intro?utm_source=chatgpt.com)
