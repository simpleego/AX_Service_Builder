# AX 프로덕트 기획 & 서비스 설계 - Mermaid 구조도 모음

- 과정 시간: 72시간(9일 x 8시간)
- 용도: 강의 슬라이드, Markdown 문서, Mermaid Live Editor, GitHub README에 복사해 사용
- 주의: 렌더러에 따라 `<br/>` 줄바꿈 표현이 다를 수 있습니다.

## 1. 전체 AX 풀스택 과정과의 연결

```mermaid
flowchart LR
    A[AX 프로덕트 기획<br/>서비스 설계 72h] --> B[AI-Augmented<br/>백엔드 개발]
    B --> C[도메인 모델링<br/>데이터 아키텍처]
    C --> D[API 아키텍처<br/>인증·보안]
    D --> E[AX UI 구현<br/>프론트엔드 통합]
    E --> F[AI Native<br/>테스트·CI/CD]
    F --> G[LLM 서비스 엔지니어링<br/>RAG 파이프라인]
    A -. 요구사항·와이어프레임·UT 결과 .-> E
    A -. 기능 명세·데이터 항목 .-> B
    A -. AI 가치·사용 시나리오 .-> G
```

## 2. AI 서비스 기획 전체 프로세스

```mermaid
flowchart LR
    A[문제 발견] --> B[사용자 리서치]
    B --> C[인사이트·페르소나]
    C --> D[사용자 여정 맵]
    D --> E[가치 제안·기능 명세]
    E --> F[와이어프레임]
    F --> G[Figma 프로토타입]
    G --> H[사용성 테스트]
    H --> I[개선·개발 인계]
    H -. 반복 .-> E
```

## 3. Double Diamond와 생성형 AI의 역할

```mermaid
flowchart LR
    A[발견 Discover<br/>문제·사용자 탐색] --> B[정의 Define<br/>핵심 문제 선정]
    B --> C[개발 Develop<br/>다양한 해결안 탐색]
    C --> D[전달 Deliver<br/>프로토타입·검증]
    X[생성형 AI] -. 질문 확장·자료 정리 .-> A
    X -. 패턴 후보·반론 .-> B
    X -. 아이디어·초안 .-> C
    X -. 테스트 문항·리뷰 .-> D
    R[사람의 책임] --- A
    R --- B
    R --- C
    R --- D
```

## 4. 사용자 리서치에서 페르소나까지

```mermaid
flowchart TD
    A[인터뷰·관찰 원자료] --> B[사실 단위로 분해]
    B --> C[어피니티 맵으로 군집화]
    C --> D[패턴·긴장·욕구 발견]
    D --> E[인사이트 문장]
    E --> F[페르소나]
    E --> G[기회 영역]
    H[AI 보조] -. 요약 후보·분류 후보 .-> C
    H -. 반례·누락 질문 .-> D
    I[금지] -. 가짜 인터뷰·가짜 통계 .-> A
```

## 5. 사용자 여정 맵 구성 요소

```mermaid
flowchart LR
    A[단계] --> B[사용자 행동]
    B --> C[생각·질문]
    C --> D[감정 곡선]
    D --> E[접점·채널]
    E --> F[불편·위험]
    F --> G[개선 기회]
    G --> H[AI 적용 여부·근거]
```

## 6. MoSCoW 우선순위 결정 흐름

```mermaid
flowchart TD
    A[기능 후보] --> B{핵심 사용자 가치에<br/>직접 필요한가?}
    B -- 예 --> C{없으면 서비스가<br/>성립하지 않는가?}
    C -- 예 --> M[Must]
    C -- 아니오 --> S[Should]
    B -- 아니오 --> D{비용 대비 효과가<br/>크고 여력이 있는가?}
    D -- 예 --> CO[Could]
    D -- 아니오 --> W[Won't this time]
    M --> V[수용 기준 작성]
    S --> V
    CO --> V
```

## 7. Figma 컴포넌트 계층

```mermaid
flowchart TD
    A[Design Tokens<br/>색상·타이포·간격] --> B[Base Components<br/>Button·Input·Icon]
    B --> C[Composite Components<br/>Search Bar·Card·Modal]
    C --> D[Patterns<br/>Login·Search Result·Chat]
    D --> E[Screens<br/>사용자 과업 화면]
    E --> F[Prototype<br/>상태·전환·피드백]
    G[Auto Layout] --- B
    G --- C
    H[Variants·Properties] --- B
    H --- C
```

## 8. 사용성 테스트 반복 루프

```mermaid
flowchart LR
    A[과업·성공 기준 정의] --> B[참가자 안내]
    B --> C[Think Aloud 테스트]
    C --> D[관찰·기록]
    D --> E[문제 심각도 분류]
    E --> F[개선안 우선순위]
    F --> G[프로토타입 수정]
    G --> H[재검증]
    H -. 반복 .-> C
```

## 9. 72시간 학습 흐름

```mermaid
flowchart LR
    D1[1일차<br/>문제 정의] --> D2[2일차<br/>사용자 리서치]
    D2 --> D3[3일차<br/>인사이트·페르소나]
    D3 --> D4[4일차<br/>여정 맵]
    D4 --> D5[5일차<br/>MoSCoW·명세]
    D5 --> D6[6일차<br/>IA·와이어프레임]
    D6 --> D7[7일차<br/>Figma 컴포넌트]
    D7 --> D8[8일차<br/>프로토타입]
    D8 --> D9[9일차<br/>UT·최종 인계]
```

## 10. 후속 개발 과목 인계 구조

```mermaid
flowchart TD
    A[기획 산출물] --> B[PRD·사용자 스토리]
    A --> C[화면 목록·사용자 흐름]
    A --> D[ERD 후보 데이터 항목]
    A --> E[API 입출력 초안]
    A --> F[Figma 컴포넌트·프로토타입]
    A --> G[UT 결과·우선 개선사항]
    B --> H[백엔드·API 과정]
    C --> I[React UI 과정]
    D --> J[데이터 아키텍처 과정]
    E --> H
    F --> I
    G --> K[AI Native 테스트·CI/CD]
    B --> L[LLM·RAG 시나리오]
```

## 11. 수업 운영용 핵심 프롬프트

### 리서치 질문 검토

```text
당신은 UX 리서치 코치입니다. 아래 인터뷰 질문을 검토하세요.
단, 사용자 답변이나 통계를 새로 만들지 마세요.
각 질문에 대해 다음을 표시하세요.
1. 유도 질문 여부
2. 한 질문에 두 가지를 묻는지 여부
3. 과거 행동을 묻는지 여부
4. 더 중립적인 대안 질문
5. 민감정보 최소화 여부

인터뷰 질문:
[붙여넣기]
```

### 기능 명세 리뷰

```text
아래 사용자 스토리와 수용 기준을 리뷰하세요.
코드를 생성하지 말고 명세의 누락과 모호성만 찾으세요.
정상 상태뿐 아니라 빈 상태, 오류, 권한, 로딩, AI 응답 실패를 확인하세요.
각 문제를 심각도와 수정 예시로 정리하세요.

[사용자 스토리 및 수용 기준 붙여넣기]
```

### UT 관찰 기록 합성

```text
아래 관찰 기록만을 근거로 사용성 문제 후보를 군집화하세요.
관찰되지 않은 행동이나 참가자 의도를 추측하지 마세요.
각 군집에 대해 근거 문장, 영향받은 과업, 빈도, 심각도 후보를 제시하세요.
최종 판단은 사람이 하도록 불확실성을 표시하세요.

[익명화된 관찰 기록 붙여넣기]
```
