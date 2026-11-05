# CORS 기초

CORS(Cross-Origin Resource Sharing, 교차 출처 리소스 공유)의 핵심 원리는 보안을 위해 브라우저가 기본적으로 차단하는 서로 다른 출처(Origin) 간의 자원 요청을, 서버의 허가를 받아 안전하게 허용하는 메커니즘입니다.
브라우저의 기본 보안 정책인 SOP(Same-Origin Policy, 동일 출처 정책)를 우회하여 안전하게 데이터를 주고받기 위해 고안되었습니다.

## 1. 출처(Origin)란?

브라우저는 Protocol, Host, Port 3가지가 모두 같아야 동일한 출처로 인식합니다. 이 중 하나라도 다르면 교차 출처(Cross-Origin)가 됩니다.  
• 기준 URL: https://example.com:8080  
	• https://example.com ➔ 동일 출처 (경로만 다름)  
	• http://example.com:8080 ➔ 교차 출처 (Protocol 다름)  
	• https://example.com ➔ 교차 출처 (Host 다름)  
	• https://example.com:9090 ➔ 교차 출처 (Port 다름)  

## 2. CORS의 핵심 작동 원리 (3가지 시나리오)

브라우저가 다른 출처로 HTTP 요청을 보낼 때, 요청의 종류에 따라 세 가지 방식 중 하나로 CORS를 검증합니다.

- ① 예비 요청 (Preflight Request)

가장 흔하게 사용되는 방식입니다. 브라우저는 본 요청을 보내기 전, 안전한 요청인지 확인하기 위해 OPTIONS 메서드로 예비 요청을 먼저 보냅니다.
1. 브라우저 ➔ 서버: "이런 조건(메서드, 헤더)으로 본 요청을 보내도 괜찮니?" (OPTIONS 요청 + Origin 헤더)
2. 서버 ➔ 브라우저: "응, 이 출처와 메서드는 허용할게." (Access-Control-Allow-* 헤더 응답)
3. 브라우저: 응답을 확인한 후 안전하다고 판단되면 그제야 진짜 요청(GET, POST 등)을 전송합니다.

- ② 단순 요청 (Simple Request)

예비 요청 없이 곧바로 본 요청을 보내는 방식입니다. 조건이 매우 까다로워 특정 상황에서만 발동합니다.
• 메서드가 GET, HEAD, POST 중 하나여야 합니다.
• Accept, Accept-Language, Content-Language, Content-Type 등 제한된 헤더만 사용해야 합니다.
• Content-Type은 application/x-www-form-urlencoded, multipart/form-data, text/plain만 허용됩니다. (application/json은 단순 요청이 불가하여 Preflight가 발생합니다.)

- ③ 인증된 요청 (Credentialed Request)

쿠키, 인증 토큰(Authorization 헤더) 등 보안 자격 증명을 포함한 요청을 보낼 때 사용합니다.
• 클라이언트와 서버 양측 모두 특별한 설정이 필요합니다.
• 클라이언트는 요청 시 credentials: 'include' 옵션을 설정해야 합니다.
• 서버는 응답 헤더에 반드시 Access-Control-Allow-Credentials: true를 포함해야 하며, Access-Control-Allow-Origin: *(와일드카드)을 사용할 수 없고 반드시 명확한 출처를 지정해야 합니다.

## 3. 주요 CORS 응답 헤더 (서버 설정 핵심)

CORS 문제를 해결하려면 서버에서 브라우저에게 허가증(헤더)을 쥐여주어야 합니다.
• Access-Control-Allow-Origin: 리소스 접근이 허용된 출처를 지정합니다. (예: https://myfrontend.com)
• Access-Control-Allow-Methods: 허용하는 HTTP 메서드 목록을 지정합니다. (예: GET, POST, PUT, DELETE)
• Access-Control-Allow-Headers: 예비 요청 시 허용할 커스텀 헤더를 지정합니다.
• Access-Control-Max-Age: 예비 요청(Preflight) 결과를 브라우저에 캐싱할 시간을 초 단위로 지정하여 중복 요청을 줄입니다.

## 핵심 요약

CORS는 브라우저가 주체가 되어 동작하는 보안 메커니즘입니다. 브라우저는 요청 헤더에 Origin을 담아 보내고, 서버가 응답 헤더에 Access-Control-Allow-Origin을 내려주면, 두 값이 일치하는지 브라우저가 최종 비교하여 안전성을 검증합니다. 즉, 서버가 데이터를 주더라도 브라우저가 판단하기에 허가되지 않은 출처라면 에러를 발생시키고 데이터를 파기합니다.
CORS와 관련하여 현재 겪고 계신 특정 에러가 있거나, 사용 중인 백엔드 프레임워크(Spring, Node.js, Fastify 등)에서의 구체적인 해결 방법이 궁금하시다면 언제든 말씀해 주세요!

## 다양한 예시

CORS가 실제로 어떻게 동작하고 왜 에러가 나는지, 개발하면서 가장 자주 마주치는 4가지 실무 시나리오를 통해 상세히 설명해 드릴게요.

## ① 프론트(React)와 백엔드(Node.js) 개발 중 발생하는 에러

• 상황: 로컬에서 프론트엔드와 백엔드를 띄워놓고 API를 호출하는 가장 흔한 상황입니다.
• 출처 상태:
	• 프론트엔드: http://localhost:3000
	• 백엔드 API: http://localhost:8000
	• 👉 Port가 다르므로 교차 출처(Cross-Origin)입니다.

❌ 에러 발생 시나리오

1. React 앱에서 fetch('http://localhost:8000/api/users')를 호출합니다.
2. 브라우저는 요청 헤더에 Origin: http://localhost:3000을 붙여서 서버로 보냅니다.
3. 백엔드 서버는 아무런 CORS 설정을 하지 않아서, 응답 헤더에 Access-Control-Allow-Origin이 없는 상태로 데이터를 보냅니다.
4. 브라우저의 판단: *"응답은 왔는데, 내 Origin(localhost:3000)을 허용한다는 서버의 인증서(헤더)가 없네? 이 데이터는 차단한다!"*하며 콘솔에 CORS 에러를 뿜습니다.

서버의 해결 조치

백엔드(Node.js/Express) 코드에 허가 헤더를 추가합니다.
javascript
// 모든 출처를 허용하거나, 특정 출처만 지정
res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
코드를 사용할 때는 주의가 필요합니다.

## ② application/json으로 데이터를 보낼 때 (Preflight 발생)

• 상황: 로그인이나 글 작성을 위해 서버에 JSON 데이터를 POST로 전송합니다.
• 출처 상태: 프론트(https://myweb.com) ➔ 백엔드(https://myweb.com)

🔄 실제 동작 과정 (눈에 보이지 않는 2번의 요청)

Content-Type을 application/json으로 설정하는 순간, 브라우저는 이것을 '안전함이 검증되지 않은 요청'으로 판단하여 예비 요청(Preflight)을 먼저 보냅니다.
1. 1차 요청 (OPTIONS - 예비 요청):
	• 브라우저가 서버에 "나 이제 POST로 JSON 보낼 건데 괜찮아?" 하고 물어봅니다.
	• 요청 헤더: Access-Control-Request-Method: POST, Origin: https://myweb.com
2. 1차 응답 (서버의 허가):
	• 서버가 "응, 그 출처랑 메서드 허용해!" 하고 응답합니다.
	• 응답 헤더: Access-Control-Allow-Origin: https://myweb.com, Access-Control-Allow-Methods: POST
3. 2차 요청 (POST - 본 요청):
	• 예비 요청이 통과되면, 브라우저가 비로소 진짜 사용자의 데이터(JSON)를 담아 POST 요청을 보냅니다.
💡 실무 팁: 네트워크 창을 열었을 때 똑같은 API가 연속으로 2번 찍히고 하나는 OPTIONS라고 되어 있다면, 이 Preflight 과정을 거치고 있는 것입니다.

## ③ 로그인 쿠키를 주고받을 때 (Credentialed Request)

• 상황: 사용자가 로그인을 한 후, 브라우저가 백엔드에 요청을 보낼 때마다 자동으로 세션 쿠키나 인증 정보를 포함해서 보내야 합니다.
• 출처 상태: 프론트(https://service.com) ➔ 백엔드(https://service.com)

🔐 가장 까다로운 보안 규칙

보안 자격 증명(쿠키 등)이 포함되면 브라우저와 서버는 훨씬 엄격한 규칙을 적용합니다.
• 클라이언트 설정: 요청할 때 반드시 credentials: 'include' 옵션을 켜야 쿠키가 날아갑니다.
• 서버 설정 (여기서 제일 많이 틀립니다):
	1. 응답 헤더에 반드시 Access-Control-Allow-Credentials: true를 명시해야 합니다.
	2. [주의] Access-Control-Allow-Origin: * (와일드카드)는 절대로 허용되지 않습니다. 쿠키를 주고받을 때는 보안상 출처를 뭉뚱그릴 수 없기 때문입니다. 반드시 https://service.com 처럼 정확한 주소 하나를 명시해야 합니다.

## ④ 오픈 API나 CDN을 쓸 때는 왜 에러가 안 날까?

• 상황: 기상청 날씨 API를 쓰거나, 이미지 주소(https://unsplash.com...)를 가져와 쓸 때.
• 출처 상태: 내 사이트(http://localhost:3000) ➔ 오픈 API 서버

🔓 전면 개방 정책

오픈 API나 기상청 데이터, CDN 같은 서비스들은 전 세계 누구나 가져가서 써야 하는 리소스입니다.
따라서 이들 서버의 응답 헤더를 열어보면 백엔드 개발자가 아래와 같이 설정해 두었습니다.
• Access-Control-Allow-Origin: *
이 와일드카드(*) 표시 덕분에 브라우저는 어떤 사이트에서 요청을 보내든 간에 차단하지 않고 곧바로 데이터를 통과시켜 줍니다.

⚠️ 개발자들이 흔히 하는 착각과 진실

• 착각: "CORS 에러가 났으니 서버가 터졌거나 내 요청이 서버에 안 갔겠지?"
• 진실: 서버는 요청을 정상적으로 받아서 200 OK와 함께 데이터를 다 돌려주었습니다. 다만 응답을 받은 브라우저가 헤더를 검사한 뒤 규격에 맞지 않아 데이터를 파기하고 에러를 띄운 것입니다. (서버 로그를 보면 멀쩡히 작동하고 있습니다.)
• 착각: "Postman이나 curl로 요청할 때는 데이터가 잘 나오는데 왜 React 코드로 짜면 에러가 나죠?"
• 진실: CORS는 브라우저(크롬, 사파리 등)가 사용자 보호를 위해 강제하는 보안 정책입니다. 브라우저가 아닌 Postman, 모바일 앱, 서버 대 서버 통신에서는 CORS 정책이 아예 적용되지 않습니다.
다양한 예시 중 현재 구현 중이거나 해결해야 하는 시나리오(예: 쿠키 전송, JSON 통신 등)가 있으신가요?
어떤 백엔드 언어/프레임워크를 쓰고 계시는지 알려주시면 바로 적용할 수 있는 구체적인 서버 설정 코드를 짜드릴 수 있습니다.

