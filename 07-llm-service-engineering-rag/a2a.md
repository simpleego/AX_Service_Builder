
# Agent 구조  

<img width="1060" alt="image" src="a2a.gif" />


<img width="1448" height="1086" alt="image" src="https://github.com/user-attachments/assets/f105d20b-0ae6-4bbb-97db-25988148fcca" />




# Agent Card  
<img width="1408" height="768" alt="image" src="https://github.com/user-attachments/assets/970baaf9-27cf-4ddd-897a-81de32b4576d" />

# Agent Card 구성요소
| 항목 | 설명 | 예시 |
| :--- | :--- | :--- |
| 에이전트 정체성 | 이름, 설명, 버전 정보 | `"name": "Travel Booking Agent"`,<br>`"description": "항공권 및 호텔 예약 전문 에이전트"` |
| 서비스 엔드포인트 | 에이전트와 통신할 수 있는 URL | `"url": "https://api.travel-agent.com/a2a"` |
| 능력(Capabilities) | 스트리밍, 푸시 알림 지원 여부 등 | `"streaming": true, "pushNotifications": true` |
| 스킬(Skills) | 수행 가능한 구체적인 작업 목록 | `"id": "flight-search", "id": "hotel-booking"` |
| 인증 요구사항 | 지원하는 보안 방식 | `"type": "oauth2", "type": "apiKey"` |
| 지원 모달리티 | 처리 가능한 데이터 타입 | `"inputModes": ["text", "file"]`,<br>`"outputModes": ["text", "file"]` |

# Agent Card JSON format
```json
{
  "name": "Travel Booking Agent",
  "description": "항공권 검색, 호텔 예약, 여행 일정 관리를 수행하는 전문 에이전트입니다.",
  "version": "1.0.0",
  "protocolVersion": "0.3",
  "url": "https://api.travel-agent.com/a2a",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true
  },
  "skills": [
    {
      "id": "flight-search",
      "name": "항공권 검색",
      "description": "출발지, 목적지, 날짜를 기반으로 최적의 항공권을 검색합니다."
    },
    {
      "id": "hotel-booking",
      "name": "호텔 예약",
      "description": "목적지와 일정에 맞는 호텔을 검색하고 예약합니다."
    },
    {
      "id": "itinerary-planning",
      "name": "여행 일정 생성",
      "description": "여행지의 관광명소, 맛집 등을 포함한 일정을 생성합니다."
    }
  ],
  "inputModes": ["text", "file"],
  "outputModes": ["text", "file"],
  "authentication": {
    "schemes": [
      {
        "type": "oauth2",
        "authorizationUrl": "https://auth.travel-agent.com/authorize",
        "tokenUrl": "https://auth.travel-agent.com/token",
        "scopes": ["read", "write", "booking"]
      }
    ]
  }
}
```
