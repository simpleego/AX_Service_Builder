# Agent2Agent(A2A)
> A2A의 핵심 흐름인 **① Agent Card 조회(Discovery) → ② 작업 위임(Task 생성·실행) → ③ 상태 및 산출물(Artifact) 수신**을 로컬에서 바로 실행해 볼 수 있는 **FastAPI 기반 미니멀 예제**입니다. 외부 라이브러리 없이 `fastapi`와 `uvicorn`, `httpx`만 있으면 바로 테스트할 수 있습니다.

---

### 1. 실행 환경 준비

```bash
pip install fastapi uvicorn httpx

```

---

### 2. 원격 에이전트 서버 (`remote_agent.py`)

여행 예약/일정 안내를 담당하는 **A2A Server**입니다. 내부 구현(도구·프롬프트)은 숨긴 채 `/.well-known/agent-card.json`으로 명함을 공개하고, `/a2a/tasks`로 들어온 작업을 처리해 `Task` 상태와 `Artifact`를 반환합니다.

```python
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Travel A2A Server")

# 인메모리 Task 저장소
TASKS: dict[str, dict] = {}


class MessagePart(BaseModel):
    kind: str = "text"
    text: str


class TaskRequest(BaseModel):
    message: dict


@app.get("/.well-known/agent-card.json")
def get_agent_card():
    """클라이언트가 탐색하는 Agent Card"""
    return {
        "name": "Travel Booking Agent",
        "description": "항공권 검색, 호텔 예약, 여행 일정을 안내하는 원격 에이전트",
        "version": "1.0.0",
        "url": "http://localhost:8001/a2a/tasks",
        "capabilities": {
            "streaming": False,
            "pushNotifications": False,
        },
        "defaultInputModes": ["text"],
        "defaultOutputModes": ["text"],
        "skills": [
            {
                "id": "itinerary-planning",
                "name": "여행 일정 추천",
                "description": "도시와 일정을 기반으로 추천 코스를 생성합니다.",
                "examples": ["2박 3일 도쿄 여행 일정 추천해줘"],
            }
        ],
    }


@app.post("/a2a/tasks")
def create_and_run_task(req: TaskRequest):
    """클라이언트로부터 작업을 위임받아 실행하고 Task 결과를 반환"""
    task_id = f"task-{uuid.uuid4().hex[:8]}"
    parts = req.message.get("parts", [])
    user_text = " ".join(p.get("text", "") for p in parts if p.get("kind") == "text")

    # 실제 서비스라면 내부 LLM/도구/외부 API를 호출하는 영역(클라이언트에는 비공개)
    if "도쿄" in user_text:
        plan = "1일차: 시부야·하라주쿠 / 2일차: 아사쿠사·우에노 / 3일차: 긴자·오다이바"
    else:
        plan = f"'{user_text}' 요청에 맞춘 2박 3일 핵심 명소 및 맛집 투어 일정을 구성했습니다."

    task = {
        "id": task_id,
        "status": {"state": "completed"},
        "artifacts": [
            {
                "artifactId": f"art-{uuid.uuid4().hex[:6]}",
                "name": "recommended_itinerary",
                "parts": [{"kind": "text", "text": plan}],
            }
        ],
    }
    TASKS[task_id] = task
    return task


@app.get("/a2a/tasks/{task_id}")
def get_task(task_id: str):
    """생성된 Task 상태 조회"""
    return TASKS.get(task_id, {"error": "Task not found"})

```

---

### 3. 클라이언트 에이전트 (`client_agent.py`)

원격 에이전트의 `Agent Card`를 먼저 읽어서 스킬과 엔드포인트를 확인한 뒤, `Task`를 전송하고 결과 `Artifact`를 출력하는 **A2A Client**입니다.

```python
import json
import httpx

BASE_URL = "http://localhost:8001"


def run_a2a_demo(user_request: str):
    with httpx.Client(timeout=10.0) as client:
        # 1. Discovery: Agent Card 조회
        card_res = client.get(f"{BASE_URL}/.well-known/agent-card.json")
        card_res.raise_for_status()
        agent_card = card_res.json()

        print("=== [1] Discovery: Agent Card 확인 ===")
        print(f"에이전트 이름: {agent_card['name']}")
        print(f"엔드포인트: {agent_card['url']}")
        print("보유 스킬:", [s["id"] for s in agent_card["skills"]])

        # 2. Task 위임: Message(Part) 형태로 작업 전송
        payload = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": user_request}],
            }
        }
        task_res = client.post(agent_card["url"], json=payload)
        task_res.raise_for_status()
        task = task_res.json()

        print("\n=== [2] Task 실행 및 결과 수신 ===")
        print(f"Task ID: {task['id']} | 상태: {task['status']['state']}")

        # 3. Artifact 추출
        for artifact in task.get("artifacts", []):
            for part in artifact.get("parts", []):
                if part.get("kind") == "text":
                    print(f"산출물 ({artifact['name']}): {part['text']}")

        print("\n=== [참고] 원본 Task JSON ===")
        print(json.dumps(task, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    run_a2a_demo("2박 3일 도쿄 여행 일정 추천해줘")

```

---

### 4. 실행 및 확인 방법

터미널 두 개를 열고 순서대로 실행해 보세요.

1. **원격 에이전트 서버 실행**
```bash
uvicorn remote_agent:app --reload --port 8001

```


2. **클라이언트 에이전트 실행**
```bash
python client_agent.py

```



### 이 코드로 체감할 수 있는 핵심 포인트

* **블랙박스 협업:** `client_agent.py`는 원격 에이전트가 내부적으로 어떤 규칙이나 LLM을 쓰는지 알 필요 없이, `Agent Card`의 `url`과 `skills`만 보고 작업을 넘깁니다.
* **데이터 구조 분리:** 대화 요청은 `Message`와 `Part`로 감싸 보내고, 작업 추적은 `Task` 상태(`completed`), 최종 결과물은 `Artifact`로 분리되어 돌아옵니다.

실제 서비스처럼 SSE 스트리밍(`StreamingResponse`)으로 진행 상황을 실시간 전송하는 버전이나, **오케스트레이터가 여러 에이전트 카드 중 하나를 골라 위임하는 구조**로도 확장해 볼 수 있습니다. 어떤 방향으로 발전시켜 볼까요?
