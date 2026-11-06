# CORS 기초 개념과 동작 원리

참고: [MDN 공식 문서 – Cross-Origin Resource Sharing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

CORS는 React와 같은 프론트엔드에서 FastAPI 같은 백엔드 서버에 데이터를 요청할 때 반드시 이해해야 하는 웹 보안 개념입니다.

## 1. CORS란 무엇인가?

CORS(Cross-Origin Resource Sharing) 는 서로 다른 출처(Origin) 사이에서 데이터를 공유할 수 있도록 서버가 브라우저에 허용 여부를 알려주는 HTTP 기반 메커니즘입니다.

쉽게 비유하면 다음과 같습니다.

- 브라우저: 건물의 보안 담당자
- 프론트엔드: 방문객
- 백엔드 서버: 방문하려는 사무실
- CORS 설정: 사무실에서 제공하는 방문 허용 명단

브라우저는 다른 출처로 요청한 데이터가 도착하더라도, 서버가 허용하지 않았다면 JavaScript가 그 응답을 읽지 못하도록 제한합니다.

## 2. CORS가 왜 필요한가?

React와 FastAPI의 요청 예시

React는 `http://localhost:5173`, FastAPI는 `http://localhost:8000`에서 실행된다고 가정하겠습니다.

두 프로그램은 같은 컴퓨터에서 실행되지만 포트번호가 다르므로 서로 다른 출처입니다.

브라우저가 서로 다른 출처 간의 요청을 아무런 제한 없이 허용한다면, 악성 사이트의 JavaScript가 사용자가 로그인한 다른 사이트의 민감한 응답 데이터를 읽을 위험이 있습니다.

이를 방지하기 위해 브라우저에는 SOP(Same-Origin Policy, 동일 출처 정책) 가 있으며, CORS는 서버가 허용한 경우에 한해 이 제한을 완화하는 방법입니다.

## 3. 출처(Origin)를 구분하는 기준

출처는 다음 세 가지 요소로 결정됩니다.

http\://

프로토콜

localhost

호스트

:5173

포트

세 요소가 모두 같아야 동일 출처(Same Origin)

기준 주소: `http://localhost:5173`

| 비교 주소                         | 동일 출처?    | 이유       |
| ----------------------------- | --------- | -------- |
| `http://localhost:5173/users` | &#x20;예   | 경로만 다름   |
| `http://localhost:8000`       | &#x20;아니요 | 포트가 다름   |
| `https://localhost:5173`      | &#x20;아니요 | 프로토콜이 다름 |
| `http://127.0.0.1:5173`       | &#x20;아니요 | 호스트가 다름  |

핵심은 프로토콜, 호스트, 포트 중 하나라도 다르면 Cross-Origin이라는 것입니다.

## 4. CORS의 기본 동작 과정

가장 단순한 GET 요청을 예로 들어보겠습니다.

1. React가 FastAPI에 데이터를 요청합니다.
2. 브라우저는 요청의 출처를 `Origin` 헤더로 알립니다.
3. FastAPI는 허용할 출처를 `Access-Control-Allow-Origin` 응답 헤더로 알려줍니다.
4. 브라우저가 응답 헤더를 검사하여 JavaScript의 데이터 접근을 허용하거나 차단합니다.

예를 들어 서버가 다음 헤더를 반환한다면,

```
Access-Control-Allow-Origin: http://localhost:5173
```

React에서 정상적으로 응답 데이터를 사용할 수 있습니다.

반대로 허용 헤더가 없거나 요청 출처와 일치하지 않으면 브라우저가 응답 접근을 차단합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://developer.mozilla.org\&sz=32)

MDN+1



## 5. CORS 요청에는 두 가지 대표적인 흐름이 있다

① 단순 요청(Simple Request)

브라우저

GET 요청

응답 + CORS 헤더

서버

브라우저가 별도의 사전 확인 없이 실제 요청을 전송하고, 응답의 CORS 헤더를 검사합니다. 일반적인 GET 요청이 대표적인 예입니다.

② 사전 요청(Preflight Request)

브라우저

OPTIONS 사전 요청

허용 여부 응답

실제 POST 등 요청

서버

브라우저가 먼저 `OPTIONS` 요청으로 서버에 허용 여부를 확인한 다음, 허용되면 실제 요청을 전송합니다.

예를 들어 `Content-Type: application/json`을 사용하는 POST 요청은 일반적으로 사전 요청이 발생합니다.

주의: 모든 POST 요청에 사전 요청이 발생하는 것은 아닙니다. 요청 메서드와 헤더 등의 조건에 따라 결정됩니다.

## 6. FastAPI에서 CORS를 해결하는 방법

FastAPI에는 `CORSMiddleware`가 제공됩니다. 이를 설정하면 서버가 필요한 CORS 응답 헤더를 처리합니다.

```
from fastapi import FastAPIfrom fastapi.middleware.cors import CORSMiddlewareapp = FastAPI()# 허용할 프론트엔드 출처app.add_middleware(    CORSMiddleware,    allow_origins=["http://localhost:5173"],    allow_credentials=True,    allow_methods=["*"],    allow_headers=["*"],)@app.get("/users")def get_users():    return {"name": "홍길동"}
```

설정 항목의 의미는 다음과 같습니다.

| 설정                  | 의미                  |
| ------------------- | ------------------- |
| `allow_origins`     | 접근 허용 출처            |
| `allow_credentials` | 쿠키 등 자격 증명 포함 요청 허용 |
| `allow_methods`     | 허용할 HTTP 메서드        |
| `allow_headers`     | 허용할 요청 헤더           |

여기서 `*`는 모두 허용한다는 의미입니다. 다만 `allow_origins=["*"]`는 인증 정보를 사용하는 환경에서는 적합하지 않습니다. 실제 서비스에서는 필요한 출처와 메서드만 명시하는 것이 좋습니다.

## 7. CORS에 대해 반드시 기억해야 할 내용

- CORS는 서버가 허용 여부를 알려주고 브라우저가 검사하는 구조입니다.
- CORS 오류는 반드시 서버 요청 실패를 뜻하지 않습니다. 서버에서 처리했더라도 브라우저가 응답 접근을 차단할 수 있습니다.
- CORS는 인증이나 접근 권한 검사를 대신하지 않습니다.
- Postman이나 Python `requests`는 일반적인 브라우저 CORS 정책을 적용하지 않으므로 브라우저와 결과가 다를 수 있습니다.

한 문장으로 정리하면: CORS는 서로 다른 출처의 프론트엔드가 백엔드의 응답 데이터를 읽어도 되는지를 서버가 알려주고 브라우저가 판단하는 규칙입니다.
