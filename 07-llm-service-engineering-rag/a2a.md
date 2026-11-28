
# Agent 구조  

<img width="1060" alt="image" src="a2a.gif" />


# Agent Card  
<img width="1408" height="768" alt="image" src="https://github.com/user-attachments/assets/970baaf9-27cf-4ddd-897a-81de32b4576d" />

| 항목 | 설명 | 예시 |
| :--- | :--- | :--- |
| 에이전트 정체성 | 이름, 설명, 버전 정보 | `"name": "Travel Booking Agent"`,<br>`"description": "항공권 및 호텔 예약 전문 에이전트"` |
| 서비스 엔드포인트 | 에이전트와 통신할 수 있는 URL | `"url": "https://api.travel-agent.com/a2a"` |
| 능력(Capabilities) | 스트리밍, 푸시 알림 지원 여부 등 | `"streaming": true, "pushNotifications": true` |
| 스킬(Skills) | 수행 가능한 구체적인 작업 목록 | `"id": "flight-search", "id": "hotel-booking"` |
```[cite: 2]
