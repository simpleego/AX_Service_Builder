# SDD(Spec-Driven Development)

SDD(Spec-Driven Development, 스펙 주도 개발)는 코드를 직접 작성하기 전에 명세(Spec)를 먼저 체계적으로 정의하고, 이를 바탕으로 AI 에이전트가 코드를 생성하도록 제어하는 소프트웨어 개발 방법론입니다. [1] (https://news.hada.io/topic?id=23776), [2] (https://charstring.tistory.com/1793)
AI에게 무작위로 프롬프트를 입력해 코드를 얻는 이른바 '바이브 코딩(Vibe Coding)'의 맥락 손실(Context Rot)과 일관성 저하 문제를 해결하기 위해 등장했습니다. [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [2] (https://tsyang.tistory.com/224)

---

<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/6257d964-2748-4563-a7ef-51cad36e4185" />

---


1. 핵심 개념과 특징

• 단일 진실 공급원(SSoT, Single Source of Truth): 과거에는 코드가 진실이었으나, SDD에서는 명세 문서(Spec)가 프로젝트의 유일한 진실 기준이 됩니다. [1] (https://wikidocs.net/blog/@itlab/5203/), [2] (https://www.youtube.com/watch?v=NGI9ktGm6EE&t=18)
• 역할의 변화: 개발자의 역할이 직접 코드를 타이핑하는 '코드 작성자'에서 AI의 방향을 조율하고 명세를 검증하는 '의도 설계자 및 조향사'로 이동합니다. [1] (https://news.hada.io/topic?id=27675), [2] (https://wikidocs.net/blog/@itlab/5203/)
• 주요 도구: GitHub의 Spec-kit, AWS Kiro IDE, Tessl 등이 대표적인 SDD 기반 도구입니다. [1] (https://goddaehee.tistory.com/405), [2] (https://news.hada.io/topic?id=23776)

2. 표준 워크플로우 (6단계 프로세스)

Spec-kit 등에서 사용하는 대표적인 SDD 프로세스는 다음과 같습니다: [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/)
1. Constitution (헌법): 프로젝트 전체에 적용되는 불변의 규칙과 코딩 컨벤션, 테스트 요구사항 등을 정의합니다. [1] (https://tsyang.tistory.com/224), [2] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/)
2. Specify (명세): '어떻게(How)'가 아닌 '무엇을(What)'과 '왜(Why)'의 관점에서 기능 요구사항을 작성합니다. [1] (https://tsyang.tistory.com/224), [2] (https://wikidocs.net/blog/@itlab/5203/)
3. Clarify (명확화): 명세 중 애매하거나 불확실한 부분을 식별하여 AI나 기획자와 문답을 통해 요구사항을 구체화합니다. [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [2] (https://tsyang.tistory.com/224)
4. Plan (계획): 헌법과 명세를 기반으로 기술 스택, 아키텍처, 데이터 모델 등 구체적인 구현 계획을 수립합니다. [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [2] (https://tsyang.tistory.com/224)
5. Tasks (작업 분할): 계획을 AI 에이전트가 순차적 또는 병렬로 처리할 수 있는 단위 작업으로 쪼갭니다. [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [2] (https://tsyang.tistory.com/224)
6. Implement (구현): AI 에이전트가 정의된 작업 목록과 명세에 맞춰 실제 코드를 생성하고, 개발자는 이를 검토합니다. [1] (https://velog.io/@scy512/SDDSpecification-Driven-Development-spec-kit%EB%A1%9C-%EB%B0%94%EC%9D%B4%EB%B8%8C%EC%BD%94%EB%94%A9%ED%95%98%EA%B8%B0), [2] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/)

3. 장점과 한계점


장점

• 코드 일관성 유지: AI가 맥락을 잃거나 앞뒤가 맞지 않는 코드를 생성하는 것을 방지합니다.
• 추적 가능성 및 협업: 기획자, 디자이너, 개발자가 명세 문서를 기준으로 명확하게 소통할 수 있습니다.
• 레거시 및 대규모 시스템 적합: 복잡한 비즈니스 로직이나 대규모 프로젝트에서 기술 부채가 쌓이는 것을 억제합니다. [1] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [2] (https://tsyang.tistory.com/224), [3] (https://goddaehee.tistory.com/405), [4] (https://charstring.tistory.com/1793), [5] (https://wikidocs.net/blog/@itlab/5203/)

한계점

• 초기 오버헤드: 간단한 버그 수정이나 작은 프로토타입에는 헌법·명세·계획 작성 단계가 지나치게 무겁고 번거롭게 느껴질 수 있습니다.
• 토큰 소모 및 학습 곡선: 문서가 대량으로 생성되며, AI 도구 파이프라인에 적응하기 위한 학습이 필요합니다.
• AI의 지시 불이행: 명세를 정의해도 AI가 간혹 지시를 무시하는 비정규성(Nondeterminism) 문제가 발생할 수 있습니다. [1] (https://news.hada.io/topic?id=23776), [2] (https://tsyang.tistory.com/224), [3] (https://tech.kakaopay.com/post/ifkakao-agentic-coding/), [4] (https://goddaehee.tistory.com/405)
SDD 방법론에 대해 더 알아보고 싶으시다면 다음 중 어떤 부분이 궁금하신가요?
• 특정 도구(Spec-kit 또는 Kiro)의 사용법 및 설정 방법
• 기존 TDD(테스트 주도 개발)와의 구체적인 연계 방식
• 우리 팀 프로젝트에 SDD를 도입하기 위한 적용 전략
