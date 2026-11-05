

CORS(Cross-Origin Resource Sharing, 교차 출처 리소스 공유)의 핵심 원리는 보안을 위해 브라우저가 기본적으로 차단하는 서로 다른 출처(Origin) 간의 자원 요청을, 서버의 허가를 받아 안전하게 허용하는 메커니즘입니다.
브라우저의 기본 보안 정책인 SOP(Same-Origin Policy, 동일 출처 정책)를 우회하여 안전하게 데이터를 주고받기 위해 고안되었습니다.

1. 출처(Origin)란?

브라우저는 Protocol, Host, Port 3가지가 모두 같아야 동일한 출처로 인식합니다. 이 중 하나라도 다르면 교차 출처(Cross-Origin)가 됩니다.
• 기준 URL: https://example.com:8080
	• https://example.com ➔ 동일 출처 (경로만 다름)
	• http://example.com:8080 ➔ 교차 출처 (Protocol 다름)
	• https://example.com ➔ 교차 출처 (Host 다름)
	• https://example.com:9090 ➔ 교차 출처 (Port 다름)

2. CORS의 핵심 작동 원리 (3가지 시나리오)

브라우저가 다른 출처로 HTTP 요청을 보낼 때, 요청의 종류에 따라 세 가지 방식 중 하나로 CORS를 검증합니다.

① 예비 요청 (Preflight Request)

가장 흔하게 사용되는 방식입니다. 브라우저는 본 요청을 보내기 전, 안전한 요청인지 확인하기 위해 OPTIONS 메서드로 예비 요청을 먼저 보냅니다.
1. 브라우저 ➔ 서버: "이런 조건(메서드, 헤더)으로 본 요청을 보내도 괜찮니?" (OPTIONS 요청 + Origin 헤더)
2. 서버 ➔ 브라우저: "응, 이 출처와 메서드는 허용할게." (Access-Control-Allow-* 헤더 응답)
3. 브라우저: 응답을 확인한 후 안전하다고 판단되면 그제야 진짜 요청(GET, POST 등)을 전송합니다.

② 단순 요청 (Simple Request)

예비 요청 없이 곧바로 본 요청을 보내는 방식입니다. 조건이 매우 까다로워 특정 상황에서만 발동합니다.
• 메서드가 GET, HEAD, POST 중 하나여야 합니다.
• Accept, Accept-Language, Content-Language, Content-Type 등 제한된 헤더만 사용해야 합니다.
• Content-Type은 application/x-www-form-urlencoded, multipart/form-data, text/plain만 허용됩니다. (application/json은 단순 요청이 불가하여 Preflight가 발생합니다.)

③ 인증된 요청 (Credentialed Request)

쿠키, 인증 토큰(Authorization 헤더) 등 보안 자격 증명을 포함한 요청을 보낼 때 사용합니다.
• 클라이언트와 서버 양측 모두 특별한 설정이 필요합니다.
• 클라이언트는 요청 시 credentials: 'include' 옵션을 설정해야 합니다.
• 서버는 응답 헤더에 반드시 Access-Control-Allow-Credentials: true를 포함해야 하며, Access-Control-Allow-Origin: *(와일드카드)을 사용할 수 없고 반드시 명확한 출처를 지정해야 합니다.

3. 주요 CORS 응답 헤더 (서버 설정 핵심)

CORS 문제를 해결하려면 서버에서 브라우저에게 허가증(헤더)을 쥐여주어야 합니다.
• Access-Control-Allow-Origin: 리소스 접근이 허용된 출처를 지정합니다. (예: https://myfrontend.com)
• Access-Control-Allow-Methods: 허용하는 HTTP 메서드 목록을 지정합니다. (예: GET, POST, PUT, DELETE)
• Access-Control-Allow-Headers: 예비 요청 시 허용할 커스텀 헤더를 지정합니다.
• Access-Control-Max-Age: 예비 요청(Preflight) 결과를 브라우저에 캐싱할 시간을 초 단위로 지정하여 중복 요청을 줄입니다.

핵심 요약

CORS는 브라우저가 주체가 되어 동작하는 보안 메커니즘입니다. 브라우저는 요청 헤더에 Origin을 담아 보내고, 서버가 응답 헤더에 Access-Control-Allow-Origin을 내려주면, 두 값이 일치하는지 브라우저가 최종 비교하여 안전성을 검증합니다. 즉, 서버가 데이터를 주더라도 브라우저가 판단하기에 허가되지 않은 출처라면 에러를 발생시키고 데이터를 파기합니다.
CORS와 관련하여 현재 겪고 계신 특정 에러가 있거나, 사용 중인 백엔드 프레임워크(Spring, Node.js, Fastify 등)에서의 구체적인 해결 방법이 궁금하시다면 언제든 말씀해 주세요!
