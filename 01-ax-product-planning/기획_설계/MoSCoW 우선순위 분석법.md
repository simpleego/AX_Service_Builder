# MoSCoW 우선순위 분석법 by 딥시크

## 📚 강의 개요

| 항목 | 내용 |
|------|------|
| **강의 주제** | MoSCoW 우선순위 분석법 (MoSCoW Prioritization) |
| **강의 시간** | 90분 (이론 30분 + 실습 60분) |
| **대상** | 프로젝트 관리, 요구사항 분석, 애자일 개발 학습자 |
| **학습 목표** | MoSCoW 기법 이해, 실제 프로젝트에 적용할 수 있는 능력 배양 |

---

## 1️⃣ MoSCoW 이론 개요

### 전체 구조도

```mermaid
mindmap
  root((MoSCoW<br/>Prioritization))
    정의
      요구사항 우선순위 분석 기법
      애자일 방법론에서 활용
      비즈니스 가치 중심 평가
    구성요소
      Must Have
        필수 요구사항
        없으면 시스템 실패
        법적/규제 준수
      Should Have
        중요하지만 대체 가능
        차선책 존재
        장기적 중요성
      Could Have
        바람직하지만 필수 아님
        시간/예산 여유 시 추가
        차별화 포인트
      Won't Have
        현재 단계에서 제외
        향후 재검토
        명시적 배제
    적용방법
      이해관계자 협의
      비즈니스 가치 평가
      비용-편익 분석
      리스크 평가
    장점
      의사결정 명확화
      이해관계자 합의 도출
      범위 관리 용이
      우선순위 충돌 해결
```

### MoSCoW 정의

```mermaid
flowchart LR
    subgraph "MoSCoW"
        M[Must Have<br/>반드시 해야 함]
        S[Should Have<br/>가능하면 해야 함]
        C[Could Have<br/>할 수 있으면 함]
        W[Won't Have<br/>이번에는 안 함]
    end
    
    M --> IMP[즉시 구현]
    S --> IMP2[단기 구현]
    C --> IMP3[중장기 구현]
    W --> FUT[향후 재검토]
    
    style M fill:#ff6b6b
    style S fill:#ffd93d
    style C fill:#6bcb77
    style W fill:#4d96ff
```

---

## 2️⃣ 각 카테고리 상세 설명

### Must Have (필수 요구사항)

```mermaid
flowchart TD
    subgraph "Must Have 조건"
        C1[시스템 실패 유발]
        C2[법적/규제 의무사항]
        C3[비즈니스 핵심 가치]
        C4[타 시스템 연동 필수]
        C5[보안/안전 필수]
    end
    
    C1 --> EX1[로그인 기능]
    C2 --> EX2[개인정보보호]
    C3 --> EX3[결제 처리]
    C4 --> EX4[데이터베이스 연동]
    C5 --> EX5[인증/권한 관리]
    
    style C1 fill:#ff6b6b
    style C2 fill:#ff6b6b
    style C3 fill:#ff6b6b
    style C4 fill:#ff6b6b
    style C5 fill:#ff6b6b
```

### Should Have (중요 요구사항)

```mermaid
flowchart LR
    subgraph "Should Have 특성"
        S1[중요하지만 대체 가능]
        S2[사용자 경험 향상]
        S3[장기적 비용 절감]
        S4[경쟁사 대비 필수]
    end
    
    S1 --> EX1[다크모드 지원]
    S2 --> EX2[알림 기능]
    S3 --> EX3[자동 백업]
    S4 --> EX4[소셜 로그인]
    
    style S1 fill:#ffd93d
    style S2 fill:#ffd93d
    style S3 fill:#ffd93d
    style S4 fill:#ffd93d
```

### Could Have (선택 요구사항)

```mermaid
flowchart TD
    subgraph "Could Have 특성"
        C1[시간/예산 여유 시 추가]
        C2[차별화 포인트]
        C3[일부 사용자만 필요]
        C4[대체 기술 검토 중]
    end
    
    C1 --> EX1[테마 변경 기능]
    C2 --> EX2[AI 추천 기능]
    C3 --> EX3[고급 통계]
    C4 --> EX4[실험적 기능]
    
    style C1 fill:#6bcb77
    style C2 fill:#6bcb77
    style C3 fill:#6bcb77
    style C4 fill:#6bcb77
```

### Won't Have (제외 요구사항)

```mermaid
flowchart LR
    subgraph "Won't Have 특성"
        W1[현재 단계에서 불필요]
        W2[기술적 한계]
        W3[비용 대비 효과 미미]
        W4[향후 재검토 예정]
        W5[명시적 배제로 오해 방지]
    end
    
    style W1 fill:#4d96ff
    style W2 fill:#4d96ff
    style W3 fill:#4d96ff
    style W4 fill:#4d96ff
    style W5 fill:#4d96ff
```

---

## 3️⃣ MoSCoW 적용 프로세스

### 의사결정 프로세스

```mermaid
flowchart TD
    START[요구사항 목록 수집] --> STEP1[비즈니스 가치 평가]
    STEP1 --> STEP2[구현 비용/시간 산정]
    STEP2 --> STEP3{우선순위 분류}
    
    STEP3 --> M[Must Have]
    STEP3 --> S[Should Have]
    STEP3 --> C[Could Have]
    STEP3 --> W[Won't Have]
    
    M --> V1[적절한가?]
    S --> V2[적절한가?]
    C --> V3[적절한가?]
    W --> V4[적절한가?]
    
    V1 -->|아니오| STEP3
    V2 -->|아니오| STEP3
    V3 -->|아니오| STEP3
    V4 -->|아니오| STEP3
    
    V1 -->|예| FINAL[최종 우선순위 결정]
    V2 -->|예| FINAL
    V3 -->|예| FINAL
    V4 -->|예| FINAL
    
    FINAL --> REVIEW[이해관계자 검토]
    REVIEW --> APPROVE{승인}
    APPROVE -->|승인| DONE[완료]
    APPROVE -->|반려| STEP3
```

### 의사결정 매트릭스

```mermaid
quadrantChart
    title MoSCoW 의사결정 매트릭스
    x-axis 낮은 비용 --> 높은 비용
    y-axis 낮은 가치 --> 높은 가치
    quadrant-1 Should Have
    quadrant-2 Must Have
    quadrant-3 Won't Have
    quadrant-4 Could Have
    Must-Have: [0.2, 0.8]
    Should-Have: [0.8, 0.7]
    Could-Have: [0.7, 0.2]
    Won't-Have: [0.3, 0.2]
```

---

## 4️⃣ 실습 활동

### 실습 1: 요구사항 우선순위 분류 (개인 활동)

**목표:** 주어진 20개 요구사항을 MoSCoW로 분류하기

```mermaid
flowchart LR
    subgraph "실습 데이터: 모바일 뱅킹 앱"
        R1[계좌조회]
        R2[송금/이체]
        R3[QR 결제]
        R4[생체인증]
        R5[알림센터]
        R6[다크모드]
        R7[음성인식]
        R8[해외송금]
        R9[거래내역 검색]
        R10[고객센터 채팅]
        R11[맞춤형 상품 추천]
        R12[지출 분석]
        R13[목표저축 설정]
        R14[카드 관리]
        R15[모바일 현금]
        R16[가상계좌 발급]
        R17[SNS 공유]
        R18[예금금리 조회]
        R19[보안키패드]
        R20[오프라인 결제]
    end
```

### 분류 정답 예시

```mermaid
flowchart TD
    subgraph "Must Have"
        M1[계좌조회]
        M2[송금/이체]
        M3[생체인증]
        M4[보안키패드]
        M5[거래내역 검색]
    end
    
    subgraph "Should Have"
        S1[알림센터]
        S2[QR 결제]
        S3[카드 관리]
        S4[예금금리 조회]
        S5[고객센터 채팅]
    end
    
    subgraph "Could Have"
        C1[다크모드]
        C2[음성인식]
        C3[해외송금]
        C4[모바일 현금]
        C5[지출 분석]
    end
    
    subgraph "Won't Have"
        W1[SNS 공유]
        W2[목표저축 설정]
        W3[맞춤형 상품 추천]
        W4[가상계좌 발급]
        W5[오프라인 결제]
    end
```

### 실습 2: 팀 기반 MoSCoW 워크숍 (그룹 활동)

```mermaid
flowchart TD
    START[팀 구성: 4-5명] --> STEP1[요구사항 50개 도출]
    STEP1 --> STEP2[개인별 분류]
    STEP2 --> STEP3[팀 토론]
    STEP3 --> STEP4[합의 도출]
    STEP4 --> STEP5[결과 발표]
    STEP5 --> STEP6[피드백 및 토론]
    
    style STEP3 fill:#ffd93d
    style STEP4 fill:#6bcb77
```

#### 워크숍 진행 가이드

```mermaid
timeline
    title 팀 워크숍 타임라인
    0-10분 : 요구사항 브레인스토밍
    10-20분 : 개인 분류 작업
    20-40분 : 팀 토론
    40-50분 : 최종 합의
    50-60분 : 발표 준비
    60-75분 : 팀 발표
    75-90분 : 종합 토론
```

### 실습 3: 실제 시나리오 분석

**시나리오:** 스타트업의 배달 앱 개발 (예산 1억원, 3개월)

```mermaid
gantt
    title 배달앱 개발 로드맵 (MoSCoW 기반)
    dateFormat YYYY-MM-DD
    axisFormat %m-%d

    section Must Have
    회원가입/로그인 :m1, 2024-01-01, 14d
    주문하기        :m2, after m1, 21d
    결제시스템      :m3, after m2, 14d
    주문추적        :m4, after m3, 14d

    section Should Have
    리뷰/평점       :s1, 2024-01-15, 21d
    찜목록          :s2, after s1, 14d
    푸시알림        :s3, after s2, 14d

    section Could Have
    쿠폰시스템      :c1, 2024-02-01, 14d
    AI 추천         :c2, after c1, 21d
    소셜공유        :c3, after c2, 14d

    section Wont Have
    해외배송        :milestone, w1, 2024-03-31, 0d
    실시간채팅      :milestone, w2, 2024-03-31, 0d
```

---

## 5️⃣ 실습 템플릿

### MoSCoW 분류 워크시트

```mermaid
flowchart LR
    subgraph "요구사항 ID"
        R1[R001]
        R2[R002]
        R3[R003]
    end
    
    subgraph "요구사항 명"
        T1[로그인]
        T2[장바구니]
        T3[다국어지원]
    end
    
    subgraph "MoSCoW"
        M[M/S/C/W]
        M2[M/S/C/W]
        M3[M/S/C/W]
    end
    
    subgraph "근거"
        J1[보안 필수]
        J2[핵심 기능]
        J3[선택 기능]
    end
    
    R1 --> T1 --> M --> J1
    R2 --> T2 --> M2 --> J2
    R3 --> T3 --> M3 --> J3
```

### 분류 결과 템플릿

| 요구사항 ID | 요구사항명 | 우선순위 | 근거 | 담당자 |
|------------|-----------|---------|------|--------|
| R-001 | 사용자 인증 | Must | 보안 필수 | 김개발 |
| R-002 | 데이터 암호화 | Must | 법적 규제 | 이보안 |
| R-003 | 대시보드 | Should | UX 핵심 | 박디자 |
| R-004 | 다크모드 | Could | 선택 기능 | 최프론 |
| R-005 | AR 필터 | Won't | 과도한 리소스 | 정기획 |

---

## 6️⃣ 평가 및 확인

### 이해도 확인 퀴즈

```mermaid
flowchart TD
    Q1[Q1: Must Have의 조건은?]
    Q2[Q2: Should와 Could의 차이는?]
    Q3[Q3: Won't Have를 명시하는 이유는?]
    Q4[Q4: MoSCoW의 가장 큰 장점은?]
    
    Q1 --> A1[시스템 실패 유발]
    Q2 --> A2[중요도 vs 시급성]
    Q3 --> A3[오해와 범위 증가 방지]
    Q4 --> A4[이해관계자 합의 도출]
```

### 실습 평가 기준

```mermaid
pie title 실습 평가 기준
    "분류 정확도" : 40
    "근거의 논리성" : 30
    "팀 협업" : 20
    "발표력" : 10
```

---

## 7️⃣ 추가 참고 자료

### MoSCoW와 다른 기법 비교

```mermaid
flowchart LR
    subgraph "우선순위 기법"
        M[MoSCoW]
        K[Kano Model]
        P[Pairwise]
        B[Business Value]
    end
    
    M --> |특징| M1[범주적 분류]
    K --> |특징| K1[고객 만족도]
    P --> |특징| P1[상대적 비교]
    B --> |특징| B1[가치 중심]
    
    M1 --> USE[애자일 프로젝트]
    K1 --> USE[제품 개발]
    P1 --> USE[의사결정]
    B1 --> USE[투자 우선순위]
```

### 실전 팁

```mermaid
mindmap
  root((MoSCoW<br/>실전 노하우))
    Must Have 관리
      최소화할 것
      명확한 정의
      대안 검토
    Should Have 전략
      시간 비례
      MVP 이후 추가
      사용자 피드백 반영
    Could Have 기회
      차별화 요소
      실험적 도입
      점진적 개선
    Won't Have 소통
      명시적 기록
      이유 설명
      재검토 시점 지정
```

---

## 📝 강의 노트

### 강의자 팁

1. **도입부 (5분)**
   - 실생활 예시로 시작 (예: 장보기 목록 우선순위)
   - MoSCoW의 유래와 필요성 설명

2. **이론 설명 (25분)**
   - 각 카테고리별 실제 사례 제시
   - 학생들의 질문 유도

3. **실습 진행 (60분)**
   - 개인 → 팀 → 전체 순으로 점진적 난이도
   - 실제 프로젝트 상황 가정

4. **마무리 (10분)**
   - 핵심 포인트 요약
   - Q&A 세션
   - 과제 부여

### 학생들이 자주 하는 질문

```mermaid
flowchart TD
    Q1["'Could'와 'Won't'의 경계는?"]
    Q2["모든 요구사항이 'Must'라고 주장할 때?"]
    Q3["이해관계자 간 의견 충돌 해결법?"]
    Q4["변경되는 우선순위는 어떻게 관리?"]
    
    Q1 --> A1[비즈니스 가치 vs 구현 비용 평가]
    Q2 --> A2[프로젝트 목표와 연계한 토론]
    Q3 --> A3[데이터 기반 의사결정]
    Q4 --> A4[정기적 재검토 및 버전 관리]
```

---

이 강의자료를 활용하여 학생들이 MoSCoW 기법을 이해하고 실제 프로젝트에 적용할 수 있는 능력을 키울 수 있습니다. 실습을 통해 이론을 체험하고, 팀 활동을 통해 협업 능력도 함께 향상시킬 수 있습니다.
