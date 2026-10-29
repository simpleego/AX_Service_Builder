# 처음으로 시작하는 FastAPI — Part 2. FastAPI 둘러보기 (강의자료)

> 원서: Bill Lubanovic, *FastAPI: Modern Python Web Development* (O'Reilly) — 3장 ~ 7장
> 예제 소스: <https://github.com/madscheme/fastapi>
> - 장별 예제: [`example/`](https://github.com/madscheme/fastapi/tree/main/example) (파일명 = 예제 번호, 예: `3-21.py` = 예제 3-21)
> - 대화형(REPL) 예제나 짧은 코드 조각은 저장소에 없는 경우가 있으므로 본 자료의 요약을 참고

---

## 0. Part 2 개요

### 성격
FastAPI를 **"1,000피트 상공에서"** 훑어보는 파트. 장마다 짧게 핵심만 다루고, 세부 사항은 Part 3(웹사이트 만들기)에서 깊이 들어간다.

### FastAPI를 떠받치는 세 기둥

```
                    ┌──────────────────────────┐
                    │         FastAPI          │  ← 3장: 요청·응답, 자동 문서
                    │  (통합 + 의존성 주입 6장)  │
                    └────────────┬─────────────┘
           ┌─────────────────────┼─────────────────────┐
           ▼                     ▼                     ▼
   Python 타입 힌트          Starlette              Pydantic
   (5장)                   (4장: ASGI, async)     (5장: 데이터 정의·검증)
```

### 장별 구성과 권장 시간

| 장 | 주제 | 핵심 키워드 | 권장 시간 |
|---|---|---|---|
| 3 | FastAPI 둘러보기 | 경로 데코레이터, Path/Query/Body/Header, 응답·상태 코드, `response_model`, `/docs` | 3h |
| 4 | 비동기, 동시성, Starlette | 프로세스·스레드·그린 스레드, 제너레이터, `async`/`await`, ASGI | 2h |
| 5 | Pydantic, 타입 힌트, 모델 | 타입 힌트, mypy, 데이터 묶음 비교, `BaseModel`, 타입·값 검증 | 2h |
| 6 | 의존성 | 의존성 주입(DI), `Depends`, 적용 범위(경로·라우터·전역) | 1.5h |
| 7 | 프레임워크 비교 | Flask, Django, 기타 프레임워크, 선택 기준 | 1h |

### 실습 환경 준비

```bash
pip install fastapi uvicorn      # 프레임워크 + 웹 서버
pip install httpie               # 터미널용 웹 클라이언트 (JSON 기본)
pip install requests httpx       # 파이썬 웹 클라이언트 (httpx는 비동기도 지원)
```

> 강의 팁: 이 책은 curl 대신 **HTTPie**를 주로 사용. 수업에서는 HTTPie, 브라우저, Postman, `/docs` 중 학생들이 편한 도구를 함께 보여 주면 좋다.

---

## 3장. FastAPI 둘러보기

### 학습 목표
- FastAPI의 특징과 구성 요소를 설명할 수 있다.
- 경로 데코레이터와 경로 함수로 엔드포인트를 만들고 Uvicorn으로 실행할 수 있다.
- 요청 데이터를 Path · Query · Body · Header에서 받는 방법을 구분해 쓸 수 있다.
- 응답 상태 코드·헤더·타입, `response_model`, 자동 문서를 활용할 수 있다.

### 3.1 FastAPI란?
- 2018년 **세바스티안 라미레스(Sebastián Ramírez)** 가 발표한, 웹 **API** 개발에 초점을 둔 현대적 Python 웹 프레임워크 (전통적인 웹 콘텐츠도 가능)

| 장점 (공식 사이트 주장) | 설명 |
|---|---|
| 성능 | 일부 경우 Node.js, Go 수준 — Python 프레임워크로는 이례적 |
| 빠른 개발 | 어색하거나 날카로운 부분이 적음 |
| 코드 품질 | 타입 힌트와 모델로 버그 감소 |
| 자동 문서·테스트 페이지 | OpenAPI 명세를 손으로 쓰지 않아도 됨 |

**구성**: Python 타입 힌트 + **Starlette**(웹 처리, async) + **Pydantic**(데이터 정의·검증) + 이를 엮는 FastAPI 고유 통합

### 3.2 첫 FastAPI 애플리케이션

```python
from fastapi import FastAPI

app = FastAPI()                 # 웹 애플리케이션 전체를 나타내는 최상위 객체

@app.get("/hi")                 # 경로 데코레이터: GET /hi 요청을 아래 함수로
def greet():                    # 경로 함수: HTTP 요청·응답의 접점
    return "Hello? World?"
```
- 소스: [`3-1.py`](https://github.com/madscheme/fastapi/blob/main/example/3-1.py), [`3-3.py`](https://github.com/madscheme/fastapi/blob/main/example/3-3.py)

| 용어 | 의미 |
|---|---|
| `app` | 최상위 FastAPI 객체 |
| 경로 데코레이터 `@app.get("/hi")` | URL + HTTP 메서드를 함수에 연결. 메서드마다 별도 함수 가능 |
| 경로 함수 `greet()` | 실제 요청을 처리하고 응답을 반환 |

**Uvicorn으로 실행하는 두 가지 방법**

| 방식 | 방법 |
|---|---|
| 외부 (명령줄) | `uvicorn hello:app --reload` (`hello` = 파일명, `app` = 객체명) |
| 내부 (코드 안) | `if __name__ == "__main__": uvicorn.run("hello:app", reload=True)` |

- `reload` : 코드가 바뀌면 서버 자동 재시작
- 기본 주소: `localhost:8000` (`host`, `port` 인자로 변경 가능)

**테스트 방법 4가지**

| 도구 | 명령 |
|---|---|
| 브라우저 | `http://localhost:8000/hi` |
| Requests | `requests.get("http://localhost:8000/hi").json()` |
| HTTPX | `httpx.get("http://localhost:8000/hi").json()` (Requests와 거의 동일) |
| HTTPie | `http localhost:8000/hi` (`-b` 본문만, `-v` 요청 헤더까지 전부) |

### 3.3 HTTP 요청 — 데이터는 어디에 있나?

HTTP 요청의 구성: **메서드 + 경로** · 쿼리 파라미터 · 헤더 · 본문(body)

FastAPI는 이를 경로 함수의 **매개변수 선언**만으로 꺼내 준다 → 이것이 **의존성 주입**(6장에서 자세히)

| 위치 | 선언 방법 | 예시 URL / 요청 | 소스 |
|---|---|---|---|
| **Path** | 데코레이터에 `{who}` + 같은 이름의 매개변수 | `GET /hi/Mom` | [`3-11.py`](https://github.com/madscheme/fastapi/blob/main/example/3-11.py) |
| **Query** | URL에 없는 매개변수 → 자동으로 쿼리로 간주 | `GET /hi?who=Mom` | [`3-15.py`](https://github.com/madscheme/fastapi/blob/main/example/3-15.py) |
| **Body** | `who: str = Body(embed=True)` | `POST /hi` + `{"who": "Mom"}` | [`3-21.py`](https://github.com/madscheme/fastapi/blob/main/example/3-21.py) |
| **Header** | `who: str = Header()` | 요청 헤더 `who: Mom` | [`3-24.py`](https://github.com/madscheme/fastapi/blob/main/example/3-24.py) |

**HTTPie 문법 정리 (강의 슬라이드용)**

| 문법 | 의미 | 예 |
|---|---|---|
| `name==value` | 쿼리 파라미터 | `http -b localhost:8000/hi who==Mom` |
| `name=value` | JSON 본문 필드 | `http -v localhost:8000/hi who=Mom` (자동으로 POST) |
| `name:value` | HTTP 헤더 | `http -v localhost:8000/hi who:Mom` |

**세부 포인트**
- 경로 문자열 `"/hi/{who}"`에 **f-string을 쓰지 말 것** — 중괄호는 FastAPI가 경로 파라미터 표시로 사용
- **GET에는 본문을 쓰지 않는다**: GET은 같은 질문에 같은 답을 주는 **멱등(idempotent)** 조회용. 본문은 생성(POST)·수정(PUT/PATCH) 시 사용
- `Body(embed=True)` : 본문을 `"Mom"`이 아니라 `{"who": "Mom"}` 형태로 기대
- 헤더 이름 변환: FastAPI는 헤더 키를 **소문자**로, 하이픈(`-`)을 **밑줄(`_`)** 로 바꿈 → `User-Agent` 헤더는 `user_agent: str = Header()`로 받음 ([`3-26.py`](https://github.com/madscheme/fastapi/blob/main/example/3-26.py))
- 한 경로 함수에서 여러 위치(경로·쿼리·본문·헤더·쿠키)를 **함께** 받을 수 있음

**어떤 방법을 언제 쓸까?**

| 방법 | 권장 용도 |
|---|---|
| URL 경로 | RESTful 규칙에 따른 리소스 식별 (ID 등) |
| 쿼리 문자열 | **선택적** 인자 (페이지네이션, 정렬 등) |
| 본문 | 큰 입력 (모델 전체 또는 일부) |

→ 어느 경우든 타입 힌트를 달면 **Pydantic이 자동으로 타입 검사**

### 3.4 HTTP 응답

- 기본: 반환값을 **JSON으로 변환**, `Content-Type: application/json`
- 기본 상태 코드 **200**, 예외는 4xx

| 항목 | 방법 | 소스 |
|---|---|---|
| 상태 코드 지정 | 데코레이터에 `status_code=201` 등 | [`3-28.py`](https://github.com/madscheme/fastapi/blob/main/example/3-28.py) |
| 응답 헤더 추가 | 매개변수 `response: Response` → `response.headers[name] = value` (반환 불필요) | [`3-30.py`](https://github.com/madscheme/fastapi/blob/main/example/3-30.py) |

**응답 타입** (`fastapi.responses`)

| 클래스 | 용도 |
|---|---|
| `JSONResponse` | 기본값 |
| `HTMLResponse` | HTML |
| `PlainTextResponse` | 일반 텍스트 |
| `RedirectResponse` | 리디렉션 |
| `FileResponse`, `StreamingResponse` | 파일 (15장) |
| `Response` (일반) | `content`, `media_type`, `status_code`, `headers`를 직접 지정 |

### 3.5 타입 변환 — `jsonable_encoder()`
- 표준 `json.dumps()`는 `datetime` 등 일부 타입에서 예외 발생
- FastAPI는 내부적으로 `jsonable_encoder()`로 먼저 "JSON 가능한" 구조로 바꾼 뒤 `json.dumps()` 호출 → Pydantic 모델도 자동 변환
- 소스: [`3-32.py`](https://github.com/madscheme/fastapi/blob/main/example/3-32.py) (pytest로 두 방식 비교)

### 3.6 모델 변형과 `response_model`

같은 데이터라도 **입력용 · 내부용 · 출력용** 모델을 나누는 경우가 많다.
- 민감 정보 제거 (예: 의료 개인정보)
- 입력에 없는 필드 추가 (예: 생성 시각)

| 모델 | 필드 | 용도 |
|---|---|---|
| `TagIn` | `tag` | 사용자가 보내는 입력 |
| `Tag` | `tag`, `created`, `secret` | 내부 저장용 (`secret`은 외부 노출 금지) |
| `TagOut` | `tag`, `created` | 사용자에게 돌려주는 출력 |

```python
@app.get("/{tag_str}", response_model=TagOut)
def get_one(tag_str: str) -> TagOut:
    tag: Tag = service.get(tag_str)
    return tag          # Tag를 반환해도 TagOut에 없는 secret은 자동 제거
```
- 소스: [`3-33.py`](https://github.com/madscheme/fastapi/blob/main/example/3-33.py) (모델), [`3-34.py`](https://github.com/madscheme/fastapi/blob/main/example/3-34.py) (엔드포인트)

### 3.7 자동 문서
- `http://localhost:8000/docs` → 코드에서 생성된 **OpenAPI 명세** 기반 문서·테스트 페이지 (Swagger UI)
- 사용법: 엔드포인트 펼치기 → **Try it out** → 값 입력 → **Execute** → Response body 확인
- 응답 영역에 **curl 명령**도 표시됨 (HTTPie보다 길다는 점을 비교해 보기)
- 엔드포인트가 수백 개로 늘어도 **항상 최신 상태인 문서**가 유지된다는 것이 큰 장점

> 강의 연계: `http://localhost:8000/openapi.json`을 Postman에 import하면 컬렉션이 자동으로 만들어진다는 것도 보여 주면 좋다.

### 3.8 복잡한 데이터
- GET/DELETE는 인자가 없거나 단순한 경우가 많지만, POST/PUT/PATCH는 복잡한 구조가 필요 → **5장 Pydantic 모델**로 해결

### 정리 & 확인 질문
- 같은 `who` 값을 경로·쿼리·본문·헤더로 보내는 방법을 각각 설명해 보자.
- GET 요청에 본문을 쓰지 않는 이유는?
- `response_model`이 보안 측면에서 주는 이점은?

---

## 4장. 비동기, 동시성, Starlette 둘러보기

### 학습 목표
- 병렬(parallel)과 동시성(concurrent) 컴퓨팅의 차이를 설명할 수 있다.
- Python의 여러 동시성 방식(프로세스·스레드·그린 스레드·콜백·async)을 비교할 수 있다.
- `async`/`await`의 동작 원리와 FastAPI에서의 사용법을 이해한다.

### 4.1 Starlette
- **톰 크리스티(Tom Christie)** 가 만든 경량 **ASGI** 프레임워크/툴킷 — FastAPI 웹 처리의 기반
- Flask의 기반인 Werkzeug와 비슷한 역할
- 핵심: 최신 비동기 웹 표준 **ASGI** 지원

| 표준 | 방식 | 대표 프레임워크 |
|---|---|---|
| WSGI | 동기 — 느린 I/O(DB·파일·네트워크)에서 **블로킹** | Flask, Django(전통) |
| **ASGI** | 비동기 — 기다리는 동안 다른 요청 처리 | Starlette, FastAPI |

→ Starlette 기반 프레임워크는 Python에서 가장 빠른 축 (Go, Node.js에 견줄 만함)

### 4.2 병렬 vs 동시성

| 구분 | 의미 | 적합한 작업 |
|---|---|---|
| **병렬 (parallel)** | 한 작업을 여러 CPU가 **동시에** 나눠 처리 | 그래픽, 머신러닝 등 계산 집약 |
| **동시성 (concurrent)** | 하나의 CPU가 여러 작업 사이를 **전환** | 파일·네트워크 대기가 많은 웹 서버 |

- 파일 읽기나 원격 서비스 호출은 CPU 계산보다 **수천~수백만 배 느림** → 웹 앱은 대기 시간이 대부분

### 4.3 Python의 동시성 방식

| 방식 | 특징 | Python 도구 |
|---|---|---|
| 분산·병렬 컴퓨팅 | 여러 CPU·머신으로 분할. 관리가 복잡하고 비쌈 | — |
| **OS 프로세스** | OS가 선점형(preemptive)으로 스케줄링. **CPU 바운드** 작업에 적합 | `multiprocessing` |
| **OS 스레드** | 한 프로세스 안의 실행 흐름. **I/O 바운드**에 권장되지만 버그 찾기 어려움 ("유령의 집") | `threading`, `concurrent.futures` |
| 그린 스레드 | 사용자 공간에서 협력형(cooperative) 동작, 표준 함수를 몽키패치 | greenlet, gevent, Eventlet |
| 콜백 | 이벤트(클릭·키 입력 등)에 함수를 연결. 코드 흐름이 "뒤집혀" 읽기 어려움 | Twisted |
| 제너레이터 | `yield`로 중간에 멈췄다가 나중에 이어서 실행 | 내장 |
| **async / await** | 대기할 때 제어권을 넘김. 스레드보다 단순하고 성능 좋음 | `asyncio` ← **FastAPI가 사용** |

- 무게: OS 프로세스 > OS 스레드 > 그린 스레드
- FastAPI는 일반 동기 함수(`def`)를 **스레드 풀**에서 실행해 준다

### 4.4 제너레이터 — async의 발판
- `return`은 리스트 전체를 한 번에 만들어 메모리를 사용
- `yield`를 쓰면 **하나씩 내주고, 어디까지 했는지 기억**했다가 다음 반복에서 이어서 실행
- `yield`가 들어 있는 함수 = **제너레이터 함수**
- "함수 중간으로 돌아가 이어서 실행"하는 능력이 async의 바탕이 됨

### 4.5 `async`, `await`, `asyncio` — "타이밍" 농담 예제

| 버전 | 동작 | 결과 |
|---|---|---|
| 동기: `time.sleep(3)` | 질문 → 3초 대기 → 답 | 답이 3초 뒤에 나옴 |
| 비동기: `await asyncio.sleep(3)` + `asyncio.gather(q(), a())` | 질문 → 기다리는 동안 답 실행 → 남은 시간 대기 | 답이 **질문 직후** 나옴 |

**이벤트 루프의 생각 (슬라이드용)**
1. `q()`의 첫 줄 실행
2. "3초 기다려야 하네? 스톱워치 켜 두고 나중에 올게"
3. 그 사이 `a()` 실행 → 답 출력
4. 다른 `await`가 없으니 `q()`로 돌아가 남은 시간 대기 → 종료

**규칙**
- 오래 기다릴 수 있는 함수 호출 앞에 `await`, 그 함수는 `async def`로 정의
- `async def` 함수를 부르는 쪽도 `await` + `async def` … **위로 계속 전파**
- `await`가 없어도 `async def`로 선언해도 무방

> **흔한 오해 (반드시 강조)**
> `async`/`await` 자체가 코드를 빠르게 만들지는 않는다. 준비 비용 때문에 오히려 약간 느릴 수도 있다.
> 목적은 **I/O 대기 시간 동안 다른 일을 하는 것**이다.

### 4.6 FastAPI와 async

```python
@app.get("/hi")
async def greet():
    await asyncio.sleep(1)      # DB 조회·웹 다운로드 같은 1초짜리 작업을 흉내
    return "Hello? World?"
```
- 소스: [`4-5.py`](https://github.com/madscheme/fastapi/blob/main/example/4-5.py), [`4-6.py`](https://github.com/madscheme/fastapi/blob/main/example/4-6.py)
- 동기 `sleep(1)`과의 차이: 기다리는 1초 동안 서버가 **다른 요청을 처리할 수 있음**
- 경로 함수는 FastAPI가 직접 호출하므로 `await`를 붙일 필요 없음
- FastAPI가 알아서 처리: **async 경로 함수 → 이벤트 루프**, **동기 경로 함수 → 스레드 풀**
  - `asyncio.run()`, `asyncio.gather()`를 직접 쓸 필요 없음

### 4.7 Starlette 직접 사용하기 (참고)
- `Starlette(routes=[Route('/hi', greeting)])` 형태로 같은 앱을 만들 수 있음
- 소스: [`4-7.py`](https://github.com/madscheme/fastapi/blob/main/example/4-7.py)
- FastAPI는 이 위에 타입 힌트·검증·자동 문서를 얹어 API 개발을 훨씬 쉽게 해 줌

### 4.8 쉬어 가기: 클루 저택 청소 (비유)

혼자 청소 업체를 운영하는데, 빨리 끝내면 보너스를 받는다. 방마다 할 일:
1. 창문 등 고정된 부분 청소
2. 가구를 복도로 옮기기
3. 카펫·바닥 청소와 왁스칠
4. 다음 중 하나
   - (a) 마를 때까지 **기다린다** → **동기** 방식, 보너스는 포기
   - (b) 바로 **다음 방으로 간다**, 마지막 방 이후 첫 방부터 가구를 되돌림 → **비동기** 방식

**교훈**: 요구 사항은 상충하거나 이상할 수 있다 · 시간 추정은 많은 요인에 좌우된다 · 작업 순서 정하기는 과학이자 예술이다

> 강의 팁: "마르는 시간" = DB·네트워크 응답 대기 시간이라고 연결해 주면 이해가 빠르다.

### 정리 & 확인 질문
- CPU 바운드 작업과 I/O 바운드 작업에는 각각 어떤 동시성 방식이 맞는가?
- `async def` 경로 함수 안에서 `time.sleep()`을 쓰면 어떤 문제가 생길까?
- FastAPI에서 `def`와 `async def` 경로 함수는 각각 어떻게 실행되는가?

---

## 5장. Pydantic, 타입 힌트, 모델 둘러보기

### 학습 목표
- Python 타입 힌트의 문법과 mypy를 이용한 정적 검사를 설명할 수 있다.
- 데이터를 묶는 여러 방법(튜플·딕셔너리·클래스·dataclass·Pydantic)을 비교할 수 있다.
- Pydantic 모델을 정의하고 타입·값 검증을 적용할 수 있다.

### 5.1 타입 힌트
- Python 변수는 객체에 붙은 **이름**일 뿐, 타입은 객체가 가진다
- 타입 힌트는 표준 `typing` 모듈로 추가된 문법 — **인터프리터는 무시**하고 실행
- 그럼 왜 쓰나? → **mypy** 같은 도구가 타입 불일치를 경고 + Pydantic·FastAPI 같은 도구가 힌트를 활용

**문법**

| 대상 | 문법 | 예 |
|---|---|---|
| 변수 | `name: type` / `name: type = value` | `thing: str = "yeti"` |
| 컬렉션 하위 타입 | `dict[keytype, valtype]` | `responses: dict[str, int]` |
| 여러 타입 중 하나 | `Union[str, int]` / (3.10+) `str \| int` | `dict[str, str \| int]` |
| 아무 타입 | `Any` | `dict[str, Any]` |
| 함수 반환 | `def f(args) -> type:` | `def get_thing() -> str:` |

**인터프리터 vs mypy**
```python
thing1: str = "yeti"
thing1 = 47          # Python은 그냥 실행, mypy는 오류 보고
```
```bash
pip install mypy
mypy stuff.py        # Incompatible types in assignment
```
- 참고: `thing0: str`처럼 값 없이 힌트만 쓴 줄은 합법이지만, 힌트 없는 `thing0`만 쓰면 `NameError`

### 5.2 데이터 묶기 — 방법 비교

예제 도메인: **크립티드**(name, country, area, description, aka)와 **탐험가**(name, country, description)

| 방법 | 접근 방식 | 장점 | 단점 |
|---|---|---|---|
| 튜플 / 리스트 | `thing[0]` | 간단 | 몇 번째가 무엇인지 기억해야 함 |
| 튜플 + 상수 오프셋 | `thing[NAME]` | 조금 더 읽기 쉬움 | 상수를 따로 관리 |
| 딕셔너리 | `thing["name"]` | 이름으로 접근 | 너무 느슨함 (키 존재·타입 검사 없음) |
| `namedtuple` | `thing[0]`, `thing.name` | 둘 다 가능 | `thing["name"]` 불가 |
| 일반 클래스 | `thing.name` | 메서드 추가 가능 | `__init__`과 `self.` 반복 타이핑 |
| `@dataclass` | `thing.name` | `self` 반복이 사라짐 | 검증·직렬화는 부족 |

**우리가 원하는 것**: 대체 타입(Union) · 누락/선택 값 · 기본값 · **데이터 검증** · JSON 등으로의 **직렬화**

> 왜 메서드가 있는 클래스가 아닌가? 여기서의 목적은 데이터 덩어리를 **계층 사이로 그대로 옮기고, 들어오고 나갈 때 검증**하는 것. 메서드는 DB에 저장하기도 어렵다.

### 5.3 대안 비교

| 도구 | 출처 | 특징 |
|---|---|---|
| dataclasses | 표준 라이브러리 | 데코레이터 방식 |
| attrs | 서드파티 | dataclasses의 상위 집합, 데코레이터 방식 |
| **Pydantic** | 서드파티, **FastAPI에 통합** | `BaseModel` **상속** 방식, **검증**이 강력, 표준 타입 힌트 문법 사용 |

- marshmallow, Voluptuous 같은 예전 검증 라이브러리보다 빠름 (예전 것들은 타입 힌트 이전에 나와 자체 문법 사용)

**Pydantic이 지정할 수 있는 검사**: 필수/선택 · 기본값 · 기대 타입 · 값 범위 · 사용자 정의 함수 검사 · 직렬화/역직렬화

### 5.4 간단한 예제 — 파일 3개

| 파일 | 역할 | 소스 |
|---|---|---|
| `model.py` | Pydantic 모델 `Creature(BaseModel)` 정의 | [`5-8.py`](https://github.com/madscheme/fastapi/blob/main/example/5-8.py) |
| `data.py` | 가짜 데이터 `_creatures: list[Creature]` + `get_creatures()` | [`5-10.py`](https://github.com/madscheme/fastapi/blob/main/example/5-10.py) |
| `web.py` | `GET /creature` → `list[Creature]` 반환 | [`5-11.py`](https://github.com/madscheme/fastapi/blob/main/example/5-11.py) |

```python
class Creature(BaseModel):
    name: str
    country: str
    area: str
    description: str
    aka: str
```
- 모든 필드가 **필수** (기본값이 없으면 반드시 값이 있어야 함)
- 키워드 인자로 생성하면 순서 무관
- `_creatures`처럼 밑줄로 시작하는 이름 + 접근 함수 → 간단한 데이터 은닉
- 모델 리스트를 반환하면 FastAPI·Starlette가 **자동으로 JSON 변환**
- 이 3파일 구조가 Part 3의 **Model / Data / Web 계층**으로 발전함

### 5.5 타입 검증
- `description`에 리스트를 넣어 `Creature(...)`를 만들면 → `ValidationError` (문자열이 필요함)
- 소스: [`5-14.py`](https://github.com/madscheme/fastapi/blob/main/example/5-14.py)
- Pydantic은 웹과 무관한 **데이터 도구** — 웹 코드 없이 단독으로 테스트 가능

### 5.6 값 검증

타입이 맞아도 값 자체에 제약을 둘 수 있다.

| 타입 | 제약 |
|---|---|
| 정수·실수 (`conint` 등) | `gt` 초과 · `lt` 미만 · `ge` 이상 · `le` 이하 · `multiple_of` 배수 |
| 문자열 (`constr`) | `min_length` · `max_length` (문자 수) · 대/소문자 변환 · 정규식 패턴 |
| 튜플·리스트·집합 | 최소·최대 요소 개수 |

**두 가지 작성법**
```python
name: constr(min_length=2)              # 제약 타입 (constrained string)
name: str = Field(..., min_length=2)    # Field 사용, ... = 필수이며 기본값 없음
```
- 빈 문자열 `""`도 유효한 `str`이므로, 이름 최소 길이 같은 제약이 필요함
- 핵심 메시지: Pydantic으로 데이터 검증을 **자동화** → Web 계층과 Data 계층 양쪽에서 유용

### 정리 & 확인 질문
- 타입 힌트는 실행에 영향이 없는데 FastAPI에서는 왜 중요한가?
- 딕셔너리 대신 Pydantic 모델을 쓰면 무엇이 좋아지는가?
- `constr(min_length=2)`와 `Field(..., min_length=2)`의 차이는?

---

## 6장. 의존성

### 학습 목표
- 의존성과 의존성 주입(DI)의 의미, 직접 의존성을 가져올 때의 문제점을 설명할 수 있다.
- `Depends`로 의존성 함수를 작성하고, 경로·라우터·전역 범위에 적용할 수 있다.

### 6.1 의존성이란?
어떤 시점에 필요한 **특정 정보**. 웹 서비스에서 흔한 예:
- HTTP 요청에서 입력 파라미터 수집
- 입력 검증
- 일부 엔드포인트의 인증·인가 확인
- 데이터 소스(DB)에서 조회
- 메트릭·로그·추적 정보 기록

### 6.2 필요한 곳에서 직접 가져오면 생기는 문제

| 문제 | 설명 |
|---|---|
| 테스트 | 의존성을 다르게 가져오는 변형을 테스트할 수 없음 |
| 숨은 의존성 | 외부 코드가 바뀌면 함수가 깨질 수 있음 |
| 코드 중복 | 사용자 조회 같은 공통 로직을 여러 함수에 반복 |
| OpenAPI 노출 | 자동 문서 페이지는 의존성 주입 정보가 있어야 만들 수 있음 |

### 6.3 의존성 주입 (Dependency Injection)
- 함수가 필요로 하는 정보를 **함수 안에서 가져오지 말고, 밖에서 넣어 준다**
- FastAPI는 한 단계 더: 의존성을 **함수 인자로 선언**하면 FastAPI가 **호출 시점에 자동 실행**하고 결과를 넣어 줌
- 사실 3장의 `Path`, `Query`, `Body`, `Header`가 모두 **내장 의존성** — 검증·형식 변환·자동 문서를 함께 제공

### 6.4 의존성 작성하기
- 의존성은 실행되는 것이므로 **호출 가능한(Callable)** 객체 — 함수 또는 클래스

```python
def user_dep(name: str, password: str):          # 의존성 함수 (경로 데코레이터 없음)
    return {"name": name, "valid": True}

@app.get("/user")
def get_user(user: dict = Depends(user_dep)) -> dict:   # 경로 함수
    return user
```
- 소스: [`6-1.py`](https://github.com/madscheme/fastapi/blob/main/example/6-1.py), [`6-2.py`](https://github.com/madscheme/fastapi/blob/main/example/6-2.py)
- 의존성 함수는 경로 함수처럼 요청 파라미터를 이해하지만, **엔드포인트가 아니라 도우미**

> **왜 `Depends()`가 필요한가? (자주 나오는 질문)**
> - `user = user_dep` → 함수 객체 자체가 들어감
> - `user = user_dep()` → 경로 함수를 **정의할 때** 한 번 호출되어 버림
> - `user = Depends(user_dep)` → **요청이 들어올 때마다** 호출됨 ✅

- 한 경로 함수에 여러 의존성을 둘 수 있음

### 6.5 의존성 적용 범위

| 범위 | 작성법 | 적용 대상 | 소스 |
|---|---|---|---|
| **단일 경로 (값 사용)** | `def pathfunc(name = Depends(depfunc))` | 해당 경로 함수 | [`6-2.py`](https://github.com/madscheme/fastapi/blob/main/example/6-2.py) |
| **단일 경로 (검사만)** | `@app.get(url, dependencies=[Depends(depfunc)])` | 반환값이 필요 없는 검사용 | [`6-3.py`](https://github.com/madscheme/fastapi/blob/main/example/6-3.py) |
| **여러 경로** | `APIRouter(..., dependencies=[Depends(depfunc)])` | 라우터 아래 모든 경로 | [`6-4.py`](https://github.com/madscheme/fastapi/blob/main/example/6-4.py) |
| **전역** | `FastAPI(dependencies=[Depends(f1), Depends(f2)])` | 앱의 모든 경로 | [`6-5.py`](https://github.com/madscheme/fastapi/blob/main/example/6-5.py) |

> 강의 연계: Part 3에서 페이지네이션 파라미터(8장), 로그인 사용자 확인(11장 `OAuth2PasswordBearer`)이 모두 이 의존성 패턴으로 구현된다는 점을 미리 예고.

### 정리 & 확인 질문
- 의존성 주입이 테스트를 쉽게 만드는 이유는?
- 인증 검사를 모든 엔드포인트에 적용하려면 어떤 범위를 쓰는가?
- `Depends(user_dep)` 대신 `user_dep()`를 기본값으로 쓰면 어떻게 되는가?

---

## 7장. 프레임워크 비교

### 학습 목표
- Flask·Django와 FastAPI의 라우팅과 요청 데이터 처리 방식을 비교할 수 있다.
- 프로젝트 성격에 따라 적절한 프레임워크를 고를 수 있다.

### 7.1 Flask
- 스스로 **마이크로프레임워크**라 부름 — 기본만 제공하고 필요한 것은 서드파티로 보충
- Django보다 작고 배우기 빠름
- **동기(WSGI)** 기반. ASGI를 지원하는 Flask 복제 프로젝트: **Quart**
- Flask 2.0부터 `@app.get` 같은 FastAPI 스타일 데코레이터 지원

**요청 데이터 처리 비교**

| 위치 | FastAPI | Flask |
|---|---|---|
| 경로 | `@app.get("/hi/{who}")` + `def greet(who: str)` | `@app.route("/hi/<who>", methods=["GET"])` |
| 쿼리 | 매개변수 `who` 선언만 | `request.args.get("who")` |
| 본문 | `who: str = Body(embed=True)` | `request.json["who"]` |
| 헤더 | `who: str = Header()` | `request.headers.get("who")` |
| JSON 응답 | 반환값 자동 변환 | `jsonify(...)` (최근 버전은 dict 자동 변환) |

- 소스: [`7-1.py`](https://github.com/madscheme/fastapi/blob/main/example/7-1.py) ~ [`7-8.py`](https://github.com/madscheme/fastapi/blob/main/example/7-8.py) (홀수 = FastAPI, 짝수 = Flask)
- 핵심 차이: Flask는 **전역 `request` 객체에서 꺼내 쓰고**, FastAPI는 **함수 인자로 선언하면 주입되며 검증·문서화까지 자동**

### 7.2 Django
- "마감이 있는 완벽주의자를 위한" 프레임워크 — Flask·FastAPI보다 크고 복잡
- **내장 ORM**, 자동 DB **관리자(admin) 페이지** → DB 비중이 큰 사이트에 유리
- 툴킷이라기보다 **모놀리식**
- 3.0부터 ASGI 지원
- 라우팅: 데코레이터 대신 **URLConf** 테이블 한 곳에서 정의
  - 장점: 모든 경로를 한눈에 / 단점: 함수만 보고는 어떤 URL인지 알기 어려움

> 저자의 경험담: 비전문가가 Django admin 페이지의 경고 메시지를 잘못 이해해 DB를 백업에서 복구해야 했던 사례 → admin 페이지 권한 관리 주의

### 7.3 그 밖의 웹 프레임워크 기능

| 기능 | 지원 현황 |
|---|---|
| 폼 | 세 프레임워크 모두 지원 |
| 파일 업로드·다운로드 | 모두 지원 (multipart) |
| 템플릿 | 모두 **Jinja** 지원, Django는 자체 템플릿 언어도 있음 |
| 서버 전송 이벤트(SSE) | FastAPI(sse-starlette), Flask(Flask-SSE), Django(Django EventStream) |
| 큐 | 외부 패키지: ZeroMQ, Celery, Redis, RabbitMQ |
| WebSocket | FastAPI(**직접 지원**), Django(Channels), Flask(서드파티) |

### 7.4 데이터베이스
- Flask와 FastAPI는 기본 패키지에 DB 기능이 없음 / Django는 DB가 핵심 기능
- Data 계층의 DB 접근 수준: 직접 SQL · 직접 NoSQL · SQL을 생성하는 **ORM** · NoSQL용 **ODM**
- **SQLAlchemy**: 직접 SQL부터 ORM까지 여러 수준 — Flask·FastAPI 개발자의 흔한 선택
- **SQLModel**: FastAPI 제작자가 만든 SQLAlchemy + Pydantic (14장)

### 7.5 추천

| 상황 | 추천 |
|---|---|
| **API 중심 서비스** | **FastAPI** |
| 빠르게 서비스 띄우기 | Flask ≈ FastAPI |
| DB 의존도가 큰 대형 사이트 | Django (배우는 시간은 더 걸림) |

**그 밖의 프레임워크**

| 이름 | 특징 |
|---|---|
| Bottle | 파일 하나짜리 초경량, 빠른 개념 증명용 |
| Litestar | FastAPI와 비슷 (ASGI/Starlette + Pydantic), 자체 설계 철학 |
| AIOHTTP | 비동기 클라이언트·서버 |
| Socketify.py | 매우 높은 성능을 내세우는 신생 프레임워크 |

### 정리 & 확인 질문
- Flask와 FastAPI에서 요청 데이터를 얻는 방식의 가장 큰 차이는?
- Django의 URLConf 방식과 데코레이터 방식의 장단점은?
- 우리 팀 프로젝트(예: 관리자 화면이 중요한 사내 시스템 / 모바일 앱용 API)에는 어떤 프레임워크가 맞을까?

---

## 부록 A. 강의 시 주의할 점 (원서 코드 vs 최신 환경)

원서는 2023년 기준(Pydantic v1)이며 인쇄된 예제에 오타가 있습니다. 시연 전 확인하세요.

| 위치 | 원서 | 수정 / 비고 |
|---|---|---|
| 3-24, 3-26 | `@app.post("/hi")`, `@app.post("/agent")` | 테스트는 본문 없는 **GET**으로 보내므로 405 오류 → `@app.get`으로 수정 |
| 3-28 | `def happy(status_code=200):` | 상태 코드는 **데코레이터**에 지정: `@app.get("/happy", status_code=200)`. 원문 코드는 `status_code`를 쿼리 파라미터로 만들 뿐 |
| 3-33 | `from pydantic import BaseClass` | `BaseModel` |
| 3-34 | `import datetime` 후 `datetime.utcnow()`, `@app.post` | `datetime.datetime.now(datetime.timezone.utc)` (`utcnow`는 3.12부터 deprecated). `app` 객체 정의가 빠져 있음 |
| 5장 본문 | 3.9 이전엔 `from typing import Str` | `Str`은 없음. `str`은 그대로 쓰고, 3.9 이전에 필요했던 것은 `List`, `Dict`, `Tuple` 등 |
| 5-8, 5-9 | 괄호·쉼표 오타 (`)` 중복, `area="Himalayas"` 뒤 쉼표 누락) | 그대로 실행하면 SyntaxError |
| 5-12 | `uvicorn creature:app` | 파일명이 `web.py`이므로 `uvicorn web:app` |
| 5-15~5-17 | Pydantic v1 오류 메시지 (`str type expected`) | v2에서는 메시지 형식이 다름 (`Input should be a valid string`) |
| 5.6 값 검증 | `regex`, `min_items`/`max_items` | Pydantic v2: `pattern`, `min_length`/`max_length`. 최신 권장 방식은 `Annotated[str, Field(min_length=2)]` |
| 5장 | "Optional이 아니면 필수" | Pydantic v2에서는 `Optional[str]`이어도 **기본값이 없으면 필수**. 선택 필드는 `str \| None = None` |
| 6-1~6-3 | `from fastapi import Params`, `name: str = Params` | `Params`는 FastAPI에 없음 → 그냥 `name: str` 또는 `Query()` |
| 6-3 | `if not name: raise` | 빈 `raise`는 RuntimeError → `raise HTTPException(status_code=401)` 등 |
| 6장 본문 | "라우터는 9장에서" | 실제로는 **8장** (Part 3) |
| 7-5, 7-6 | FastAPI 본문 예제가 쿼리 예제와 동일, Flask 본문 예제가 GET | FastAPI: `@app.post` + `Body(embed=True)`, Flask: `methods=["POST"]` |

> 위 오류들은 **"버그 찾기" 실습 과제**로 활용하기 좋습니다. 특히 3-28(상태 코드)과 6-1(`Params`)은 학생들이 개념을 확인하기에 좋은 소재입니다.

---

## 부록 B. 실습 과제 제안

1. **[3장]** `who`를 경로·쿼리·본문·헤더로 받는 엔드포인트 4개를 만들고, HTTPie·Requests·`/docs` 세 도구로 모두 테스트하기
2. **[3장]** `/docs`에 표시된 curl 명령과 HTTPie 명령을 비교하고, `openapi.json`을 Postman에 import해 보기
3. **[3장]** 사용자 모델을 `UserIn`(비밀번호 포함) / `UserOut`(비밀번호 제외)으로 나누고 `response_model`로 비밀번호가 응답에서 빠지는지 확인하기
4. **[4장]** `time.sleep(1)`을 쓰는 동기 엔드포인트와 `await asyncio.sleep(1)`을 쓰는 비동기 엔드포인트에 동시에 10개 요청을 보내 총 소요 시간 비교하기
5. **[4장]** `async def` 경로 함수 안에서 `time.sleep(1)`을 써서 서버 전체가 멈추는 현상을 직접 확인하기
6. **[5장]** `Creature` 모델에 `country`는 정확히 2글자, `name`은 2~30글자, `aka`는 선택 필드(기본값 `None`)로 제약 추가하기
7. **[5장]** 같은 데이터를 dict · dataclass · Pydantic으로 각각 표현하고, 잘못된 타입을 넣었을 때의 동작 비교하기
8. **[6장]** `skip`, `limit` 쿼리 파라미터를 받는 페이지네이션 의존성을 만들어 여러 엔드포인트에서 재사용하기
9. **[6장]** 헤더에 `X-API-Key`가 없으면 401을 반환하는 의존성을 만들어 라우터 전체에 적용하기
10. **[7장]** 같은 "Hello" API를 Flask와 FastAPI로 각각 만들고, 코드 길이와 자동 문서 유무 비교하기

---

## 부록 C. 예제 번호 ↔ 소스 파일 빠른 참조

| 장 | 저장소에 있는 예제 (`example/`) | 저장소에 없는 예제 (본 자료 요약 참고) |
|---|---|---|
| 3 | `3-1`, `3-3`, `3-11`, `3-15`, `3-21`, `3-24`, `3-26`, `3-28`, `3-30`, `3-32`, `3-33`, `3-34` | 테스트 명령 예제 (3-4 ~ 3-10 등) |
| 4 | `4-5`, `4-6`, `4-7` | 4-1 ~ 4-4 (REPL 예제: 제너레이터, 농담 예제) |
| 5 | `5-8`, `5-10`, `5-11`, `5-14` | 5-1 ~ 5-7 (데이터 묶음 비교), 5-16, 5-17 (값 검증) |
| 6 | `6-1` ~ `6-5` | — |
| 7 | `7-1` ~ `7-8` | — |

예제 폴더: <https://github.com/madscheme/fastapi/tree/main/example>

### 다음 단계
Part 2에서 익힌 개념은 Part 3에서 이렇게 이어진다.

| Part 2 개념 | Part 3에서의 쓰임 |
|---|---|
| 경로 데코레이터, Path/Query/Body | 8장 Web 계층의 CRUD 엔드포인트 |
| `model.py` / `data.py` / `web.py` 3파일 구조 | 8~10장의 Model / Web / Service / Data 계층 |
| Pydantic 모델과 검증 | 10장 422 오류, 계층 간 데이터 전달 |
| `Depends` | 8장 페이지네이션, 11장 OAuth2 인증 |
| async | 13장 성능 |
