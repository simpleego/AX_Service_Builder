오케스트레이터(클라이언트)가 **여러 원격 에이전트의 `Agent Card`를 수집한 뒤 LLM으로 적합한 에이전트를 선택하고 작업을 위임하는 구조**를 바로 실행해 볼 수 있는 예제입니다.

이해하기 쉽도록 여행 에이전트(포트 `8001`)와 **재무/예산 에이전트(포트 `8002`)** 두 개의 원격 서버를 두고, 오케스트레이터(`orchestrator.py`)가 두 `Agent Card`를 읽고 LLM이 알맞은 에이전트를 고른 뒤 A2A로 위임합니다.

---

### 1. 원격 에이전트 서버 2개 (`remote_agents.py`)

한 파일에 두 개의 FastAPI 앱(`travel_app`, `budget_app`)을 정의해 서로 다른 포트로 띄웁니다.

```python
import uuid
from fastapi import FastAPI
from pydantic import BaseModel

travel_app = FastAPI(title="Travel A2A Agent")
budget_app = FastAPI(title="Budget A2A Agent")


class TaskRequest(BaseModel):
    message: dict


# --- [원격 에이전트 1: 여행 전문] ---
@travel_app.get("/.well-known/agent-card.json")
def travel_card():
    return {
        "name": "Travel Planning Agent",
        "description": "여행지 추천, 동선 및 일정을 짜주는 에이전트",
        "version": "1.0.0",
        "url": "http://localhost:8001/a2a/tasks",
        "skills": [
            {
                "id": "itinerary-planning",
                "name": "여행 일정 생성",
                "description": "도시와 일수 기반 추천 일정을 만듭니다.",
                "examples": ["2박 3일 교토 여행 코스 짜줘"],
            }
        ],
    }


@travel_app.post("/a2a/tasks")
def travel_task(req: TaskRequest):
    text = " ".join(
        p.get("text", "") for p in req.message.get("parts", []) if p.get("kind") == "text"
    )
    return {
        "id": f"task-{uuid.uuid4().hex[:8]}",
        "status": {"state": "completed"},
        "artifacts": [
            {
                "artifactId": f"art-{uuid.uuid4().hex[:6]}",
                "name": "travel_plan",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"[Travel Agent] '{text}'에 맞춰 1일차 구시가지 산책, 2일차 사찰·맛집 탐방 일정을 생성했습니다.",
                    }
                ],
            }
        ],
    }


# --- [원격 에이전트 2: 여행 경비/예산 전문] ---
@budget_app.get("/.well-known/agent-card.json")
def budget_card():
    return {
        "name": "Travel Budget Agent",
        "description": "항공·숙박·식비 등 여행 예산 산출 및 지출 배분을 담당하는 에이전트",
        "version": "1.0.0",
        "url": "http://localhost:8002/a2a/tasks",
        "skills": [
            {
                "id": "budget-estimation",
                "name": "여행 경비 계산",
                "description": "인원, 기간, 등급에 따른 예상 경비를 계산합니다.",
                "examples": ["2인 3박 4일 오사카 여행 예산 계산해줘"],
            }
        ],
    }


@budget_app.post("/a2a/tasks")
def budget_task(req: TaskRequest):
    text = " ".join(
        p.get("text", "") for p in req.message.get("parts", []) if p.get("kind") == "text"
    )
    return {
        "id": f"task-{uuid.uuid4().hex[:8]}",
        "status": {"state": "completed"},
        "artifacts": [
            {
                "artifactId": f"art-{uuid.uuid4().hex[:6]}",
                "name": "budget_estimate",
                "parts": [
                    {
                        "kind": "text",
                        "text": f"[Budget Agent] '{text}' 기준으로 항공 40%, 숙박 30%, 식비·교통 30% 비율의 예상 경비표를 산출했습니다.",
                    }
                ],
            }
        ],
    }

```

---

### 2. LLM 기반 오케스트레이터 클라이언트 (`orchestrator.py`)

1. 등록된 원격 에이전트 URL 목록에서 `/.well-known/agent-card.json`을 병렬/순차 조회합니다.
2. 수집한 `Agent Card` 요약과 사용자 요청을 **LLM**에 전달해 **어떤 에이전트(`url`)에 위임할지 JSON 형태로 선택**하게 합니다. (`OPENAI_API_KEY`가 없으면 키워드 기반 대체 라우터로 동작합니다.)
3. 선택된 에이전트의 `url`로 A2A `Task`를 전송하고 결과 `Artifact`를 출력합니다.

```python
import json
import os
import httpx

AGENT_BASE_URLS = [
    "http://localhost:8001",
    "http://localhost:8002",
]


def discover_agents(client: httpx.Client, base_urls: list[str]) -> list[dict]:
    cards = []
    for base_url in base_urls:
        try:
            res = client.get(f"{base_url}/.well-known/agent-card.json")
            res.raise_for_status()
            cards.append(res.json())
        except httpx.HTTPError as e:
            print(f"[경고] {base_url} Agent Card 조회 실패: {e}")
    return cards


def select_agent_with_llm(client: httpx.Client, user_query: str, cards: list[dict]) -> dict:
    """수집된 Agent Card 목록을 보고 LLM이 가장 적합한 에이전트를 선택"""
    api_key = os.getenv("OPENAI_API_KEY")

    # API 키가 없을 때도 흐름을 확인할 수 있는 폴백 라우터
    if not api_key:
        if any(k in user_query for k in ["예산", "경비", "비용", "금액"]):
            selected = next((c for c in cards if "8002" in c["url"]), cards[0])
        else:
            selected = next((c for c in cards if "8001" in c["url"]), cards[0])
        return {"selected_url": selected["url"], "reason": "API 키 미설정으로 규칙 기반 선택"}

    system_prompt = (
        "당신은 A2A 오케스트레이터입니다. "
        "제공된 Agent Card 목록을 분석해 사용자 요청을 처리할 가장 적합한 에이전트 1개를 고르세요. "
        '반드시 {"selected_url": "...", "reason": "..."} 형식의 JSON만 출력하세요.'
    )
    user_payload = json.dumps(
        {"user_query": user_query, "available_agents": cards},
        ensure_ascii=False,
    )

    res = client.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_payload},
            ],
        },
    )
    res.raise_for_status()
    content = res.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def run_orchestrator(user_query: str):
    with httpx.Client(timeout=20.0) as client:
        # 1. Agent Card 수집
        cards = discover_agents(client, AGENT_BASE_URLS)
        print(f"[1] 탐색된 에이전트 수: {len(cards)}개")
        for c in cards:
            print(f"    - {c['name']} ({c['url']}) | 스킬: {[s['id'] for s in c.get('skills', [])]}")

        # 2. LLM을 통한 대상 에이전트 선택
        decision = select_agent_with_llm(client, user_query, cards)
        target_url = decision["selected_url"]
        print(f"\n[2] LLM 선택 결과 -> {target_url}")
        print(f"    선택 사유: {decision.get('reason', '')}")

        # 3. 선택된 원격 에이전트로 Task 위임
        task_payload = {
            "message": {
                "role": "user",
                "parts": [{"kind": "text", "text": user_query}],
            }
        }
        task_res = client.post(target_url, json=task_payload)
        task_res.raise_for_status()
        task = task_res.json()

        print("\n[3] 위임 결과 수신")
        for artifact in task.get("artifacts", []):
            for part in artifact.get("parts", []):
                if part.get("kind") == "text":
                    print(f"    산출물 ({artifact['name']}): {part['text']}")


if __name__ == "__main__":
    print("=== 테스트 A: 일정 요청 ===")
    run_orchestrator("2박 3일 교토 여행 일정 짜줘")

    print("\n" + "=" * 45 + "\n")

    print("=== 테스트 B: 예산 요청 ===")
    run_orchestrator("2인 3박 4일 오사카 여행 예산 계산해줘")

```

---

### 3. 실행 방법

터미널 3개를 열어 순서대로 실행해 보세요.

1. **여행 에이전트 실행 (8001 포트)**
```bash
uvicorn remote_agents:travel_app --reload --port 8001

```


2. **예산 에이전트 실행 (8002 포트)**
```bash
uvicorn remote_agents:budget_app --reload --port 8002

```


3. **오케스트레이터 실행**
```bash
# 실제 OpenAI LLM 라우팅을 쓰려면 키 설정 (미설정 시 규칙 기반 폴백으로 동작)
# export OPENAI_API_KEY="sk-..."
python orchestrator.py

```



### 구조상 핵심 포인트

* **오케스트레이터는 전문 로직을 모름:** 오케스트레이터는 일정 생성이나 예산 계산 방법을 알지 못하고, 오직 `Agent Card`의 `description`/`skills`와 `url`만 보고 **라우팅 결정과 위임**만 수행합니다.
* **확장성:** 새로운 전문 에이전트(예: 숙소 예약 에이전트, 8003 포트)가 추가되더라도 오케스트레이터의 비즈니스 로직을 고칠 필요 없이 URL을 추가하고 `Agent Card`만 잘 기술하면 LLM이 자동으로 선택 범위에 포함합니다.
