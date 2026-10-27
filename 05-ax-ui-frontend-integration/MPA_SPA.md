#  MPA(Multi Page Application)와 SPA(Single Page Application)

MPA와 SPA는 웹 애플리케이션의 '페이지 전환 방식'을 나누는 두 가지 핵심 아키텍처입니다. [1] (https://magnificent7.tistory.com/entry/SPA-vs-MPA)
MPA는 메뉴를 누를 때마다 서버에서 새 페이지를 통째로 받아오는 전통적인 연극과 같고, SPA는 무대는 그대로 두고 필요한 소품(데이터)만 바꿔 끼우는 현대적인 연극과 같습니다. [1] (https://itdaweb.com/community/spa-vs-mpa-%ED%99%88%ED%8E%98%EC%9D%B4%EC%A7%80-%EC%9A%B0%EB%A6%AC-%ED%9A%8C%EC%82%AC%EC%97%90-%EB%A7%9E%EB%8A%94-%EC%84%A0%ED%83%9D)

📊 한눈에 비교하는 MPA vs SPA

<img width="1226" height="1283" alt="image" src="https://github.com/user-attachments/assets/941cf97c-bb83-4dba-9357-1c1fe80566e1" />

| 구분 | MPA (Multiple Page Application) | SPA (Single Page Application) |
|------|----------------------------------|--------------------------------|
| 페이지 수 | 여러 개의 HTML 페이지로 구성 | 단 하나의 HTML 페이지만 존재 |
| 렌더링 방식 | 주로 SSR (서버 사이드 렌더링) | 주로 CSR (클라이언트 사이드 렌더링) |
| 화면 전환 | 새 페이지를 요청할 때마다 화면 깜빡임 발생 | 부드럽고 깜빡임 없는 UI/UX 제공 |
| 초기 로딩 | 필요한 페이지 정보만 먼저 받아오므로 빠름 | 애플리케이션의 모든 리소스를 한 번에 받아오므로 느림 |
| SEO (검색 최적화) | 완성된 HTML을 전달하므로 매우 유리 | 검색 엔진이 자바스크립트를 인식하기 어려워 불리 |
| 대표 서비스 | 아마존, 네이버 (블로그, 뉴스 등 정보형 사이트) | 구글 맵스, 넷플릭스, Gmail |


1. MPA (Multiple Page Application)

사용자가 새로운 메뉴를 클릭할 때마다 서버에 "새로운 HTML 페이지를 주세요"라고 요청하는 방식입니다. [1] (https://hanamon.kr/spa-mpa-ssr-csr-%EC%9E%A5%EB%8B%A8%EC%A0%90-%EB%9C%BB%EC%A0%95%EB%A6%AC/), [2] (https://magnificent7.tistory.com/entry/SPA-vs-MPA)
• 장점 (SEO 친화력): 서버가 이미 글자와 이미지가 채워진 완성된 HTML 문서를 주기 때문에, 구글이나 네이버 같은 검색엔진 크롤러가 사이트 내용을 쉽게 수집합니다. 검색 노출이 중요한 쇼핑몰이나 뉴스 사이트에 필수적입니다. [1] (https://p-lab.tistory.com/entry/SPA%EC%99%80-MPA-%EA%B0%9C%EB%85%90-%EB%B0%8F-%EC%9E%A5%EB%8B%A8%EC%A0%90-%EC%A0%95%EB%A6%AC), [2] (https://it-techtree.tistory.com/entry/Web-Advantage-And-Disadvantage-SPA-MPA)
• 단점 (화면 깜빡임): 페이지를 이동할 때마다 중복된 디자인(헤더, 푸터 등)까지 매번 처음부터 다시 새로고침하므로, 화면이 덜컥거리며 깜빡이는 현상이 생겨 사용자 경험(UX)이 떨어집니다. [1] (https://lsh2016.tistory.com/142), [2] (https://p-lab.tistory.com/entry/SPA%EC%99%80-MPA-%EA%B0%9C%EB%85%90-%EB%B0%8F-%EC%9E%A5%EB%8B%A8%EC%A0%90-%EC%A0%95%EB%A6%AC)

2. SPA (Single Page Application)

처음 접속할 때 텅 빈 HTML 틀과 웹을 구동할 자바스크립트 전체를 한 번에 다 다운로드받는 방식입니다. [1] (https://duyaan.tistory.com/entry/MPA%EC%99%80-SPA%EA%B0%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80), [2] (https://hanamon.kr/spa-mpa-ssr-csr-%EC%9E%A5%EB%8B%A8%EC%A0%90-%EB%9C%BB%EC%A0%95%EB%A6%AC/)
• 장점 (부드러운 UX): 초기 로딩 이후에는 페이지를 바꿀 때 전체를 새로고침하지 않습니다. 서버로부터 '바뀌어야 할 데이터(JSON 등)'만 비동기로 쏙 받아와서 화면의 필요한 부분만 싹 바꿔치기합니다. 마치 스마트폰 앱을 쓰는 것처럼 반응이 빠르고 부드럽습니다. [1] (https://f-lab.ai/insight/spa-vs-mpa-in-frontend-development), [2] (https://www.youtube.com/watch?v=sjbIRVbRzpQ&t=53), [3] (https://hanamon.kr/spa-mpa-ssr-csr-%EC%9E%A5%EB%8B%A8%EC%A0%90-%EB%9C%BB%EC%A0%95%EB%A6%AC/), [4] (https://shape-coding.tistory.com/entry/SPA-vs-MPA-%EA%B0%9C%EB%85%90%EC%A0%95%EB%A6%AC-%EB%B0%8F-%EC%9E%A5%EB%8B%A8%EC%A0%90), [5] (https://disco-biscuit.tistory.com/179)
• 단점 (무거운 첫인상과 SEO): 처음 들어올 때 무거운 자바스크립트 파일을 통째로 받기 때문에 첫 화면이 뜰 때까지 시간이 걸립니다. 또한 처음 받아오는 HTML 파일이 텅 비어있기 때문에 검색 엔진에 노출되기 어렵다는 치명적인 약점이 있습니다. [1] (https://duyaan.tistory.com/entry/MPA%EC%99%80-SPA%EA%B0%80-%EB%AC%B4%EC%97%87%EC%9D%B8%EA%B0%80), [2] (https://velog.io/@yejine2/SPASingle-Page-Application-VS-MPA)
💡 요즘의 트렌드는?
과거에는 두 아키텍처가 칼로 자르듯 나뉘었지만, 최근에는 SPA 아키텍처(React, Vue 등)를 기반으로 하면서도 서버에서 미리 화면을 그려 전달하는 Next.js, Nuxt 같은 하이브리드 프레임워크(SSR/SSG)를 활용해 두 방식의 장점을 모두 챙기는 방식이 대세로 자리 잡았습니다. [1] (https://disco-biscuit.tistory.com/179)
진행 중이신 프로젝트의 성격을 말씀해 주시면 MPA와 SPA(또는 SSR 하이브리드) 중 어떤 아키텍처가 더 알맞은 선택일지 구체적으로 추천해 드릴 수 있습니다. 어떤 서비스를 고민 중이신가요?


