# CORS 규칙

**CORS 오류는 단순히 “다른 서버에 요청했다”는 이유로 발생하지 않습니다.**  
정확히는 **브라우저가 CORS 허용을 확인해야 하는 교차 출처 요청에서, 서버의 응답이 허용 조건을 충족하지 못할 때** 발생합니다. 필요한 사전 요청인 **프리플라이트(Preflight)** 가 실패하는 경우도 포함됩니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

**1. 먼저 ‘다른 출처’인지 판단합니다**

출처(Origin)는 **프로토콜 + 호스트 + 포트**의 조합입니다. 경로나 쿼리 문자열은 출처에 포함되지 않습니다.

현재 페이지가 `http://localhost:5173`이라면 다음과 같습니다.

| 요청 주소 | 같은 출처인가? | 이유 |
|---|---|---|
| `http://localhost:5173/api/todos` | 같음 | 경로만 다름 |
| `http://localhost:8000/todos` | 다름 | 포트가 다름 |
| `https://localhost:5173/todos` | 다름 | 프로토콜이 다름 |
| `http://127.0.0.1:5173/todos` | 다름 | 호스트가 다름 |

따라서 같은 PC에서 실행하는 **React 5173번 포트 → FastAPI 8000번 포트**도 교차 출처 요청입니다. 서버가 물리적으로 같은 컴퓨터인지는 판단 기준이 아닙니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy?utm_source=chatgpt.com)

**2. 다른 출처라도, 요청 방식에 따라 CORS 검사 여부가 달라집니다**

링크에서 다루는 이미지 사례를 이해하는 핵심입니다.

| 요청 방식 | CORS 허용 필요 여부 | 의미 |
|---|---|---|
| `fetch(url)` 또는 브라우저의 Axios | 필요 | JavaScript에서 응답 데이터를 사용 |
| `<img src="외부주소">` | 일반적으로 불필요 | 이미지를 화면에 표시 |
| `<img crossorigin="anonymous" src="외부주소">` | 필요 | CORS 방식으로 이미지 요청 |
| 주소창에서 외부 URL로 이동 | 일반적인 CORS 검사 대상 아님 | 다른 페이지로 이동 |

즉, **“이미지를 화면에 표시하는 것”과 “JavaScript가 이미지 응답 데이터를 읽는 것”은 권한이 다릅니다.** 일반 `<img>`로 표시한 외부 이미지를 canvas에 그려도, CORS 허용 없이 픽셀을 읽거나 내보내는 것은 제한됩니다. 다른 보안 정책에 의한 차단은 별개입니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

**3. CORS 검사에서 실제로 무엇을 비교하나요?**

예를 들어 다음 페이지에서 API를 호출한다고 하겠습니다.

```javascript
// 현재 페이지: http://localhost:5173
fetch("http://localhost:8000/todos");
```

브라우저는 요청에 출처를 표시합니다.

```http
Origin: http://localhost:5173
```

서버는 **응답 헤더**로 해당 출처를 허용해야 합니다.

```http
Access-Control-Allow-Origin: http://localhost:5173
```

일반적인 쿠키 미포함 교차 출처 요청에서는 다음과 같이 판정합니다.

| 서버의 `Access-Control-Allow-Origin` 값 | 결과 |
|---|---|
| `http://localhost:5173` | 통과 |
| `*` | 통과 |
| 헤더 없음 | CORS 오류 |
| `http://localhost:3000` | 출처 불일치로 오류 |
| 출처 여러 개를 쉼표로 나열 | 유효하지 않은 값이므로 오류 |

이 헤더는 **프론트엔드가 요청에 추가하는 헤더가 아니라 서버가 응답에 넣는 헤더**입니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin?utm_source=chatgpt.com)

쿠키 등을 포함하도록 `credentials: "include"`를 설정했다면 조건이 더 엄격합니다.

```javascript
fetch("http://localhost:8000/todos", {
  credentials: "include"
});
```

이때는 다음 두 응답 헤더가 필요합니다.

```http
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Credentials: true
```

**`Access-Control-Allow-Origin: *`는 사용할 수 없습니다.** 실제 쿠키가 존재하는지보다 요청의 credentials 모드가 기준입니다. [fetch.spec.whatwg.org](https://fetch.spec.whatwg.org/?utm_source=chatgpt.com)

**4. 어떤 요청은 본 요청을 보내기 전에 검사합니다**

대표적으로 다음 요청은 프리플라이트가 필요합니다.

- `PUT`, `PATCH`, `DELETE` 요청
- `Content-Type: application/json`인 POST
- `Authorization` 같은 허용 목록 밖의 요청 헤더 사용

브라우저는 먼저 `OPTIONS` 요청으로 **사용할 메서드와 헤더를 서버가 허용하는지** 확인합니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)

예를 들어 JSON POST라면 다음과 같은 교환이 이루어집니다.

```http
OPTIONS /todos
Origin: http://localhost:5173
Access-Control-Request-Method: POST
Access-Control-Request-Headers: content-type
```

허용하는 서버 응답의 예입니다.

```http
HTTP/1.1 204 No Content
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: POST
Access-Control-Allow-Headers: Content-Type
```

프리플라이트가 실패하면 **본 POST는 전송되지 않습니다.** 통과한 경우에도 **본 POST 응답의 CORS 헤더를 다시 검사**합니다.

| 실패 시점 | 본 요청의 서버 처리 여부 |
|---|---|
| 프리플라이트 실패 | 본 요청을 보내지 않음 |
| 본 응답의 CORS 검사 실패 | 서버가 이미 처리했을 수 있지만 JavaScript는 응답을 읽지 못함 |

따라서 **“CORS 오류가 났으니 DB에도 저장되지 않았겠지”라고 판단하면 안 됩니다.** 서버가 `200 OK`를 반환했더라도 CORS 검사에서 실패할 수 있습니다. [fetch.spec.whatwg.org](https://fetch.spec.whatwg.org/?utm_source=chatgpt.com)

**5. 링크의 ‘캐시 때문에 발생하는 CORS 오류’도 같은 기준입니다**

글의 사례는 다음 상황입니다.

1. 일반 `<img>` 요청으로 이미지를 가져옵니다.
2. 그 응답에 CORS 허용 헤더가 없는 상태로 캐시됩니다.
3. 이후 `fetch()`가 같은 URL의 캐시된 응답을 재사용합니다.
4. 이번에는 CORS 검사가 필요하지만, 캐시된 응답에 허용 헤더가 없어 실패합니다.

즉, **캐시 자체가 오류 조건이 아니라, 재사용한 응답이 현재 요청의 CORS 허용 조건을 충족하지 못한 것**입니다. 이런 현상이 모든 이미지 캐시에서 항상 발생하는 것은 아닙니다. [inpa.tistory.com](https://inpa.tistory.com/entry/%F0%9F%8C%90-CORS-%EC%BA%90%EC%8B%9C-%EC%97%90%EB%9F%AC?utm_source=chatgpt.com)

서버가 요청의 `Origin`에 따라 허용 헤더를 다르게 반환한다면 다음 설정으로 캐시를 구분해야 합니다.

```http
Vary: Origin
```

이는 서로 다른 `Origin`에 대한 응답이 잘못 재사용되는 것을 방지하기 위한 설정입니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Access-Control-Allow-Origin?utm_source=chatgpt.com)

또한 처음부터 다음처럼 요청하면 이미지 로딩에도 CORS 검사가 적용됩니다.

```html
<img
  crossorigin="anonymous"
  src="https://example.com/image.png"
  alt="예시 이미지"
/>
```

다만 **`crossorigin`은 서버의 허용을 만들어 주는 속성이 아닙니다.** 서버가 CORS를 허용하지 않으면 이 이미지 로딩도 실패합니다. [MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS?utm_source=chatgpt.com)
