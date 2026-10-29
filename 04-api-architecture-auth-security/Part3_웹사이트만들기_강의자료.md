# 처음으로 시작하는 FastAPI — Part 3. 웹사이트 만들기 (강의자료)

> 원서: Bill Lubanovic, *FastAPI: Modern Python Web Development* (O'Reilly) — 8장 ~ 13장
> 예제 소스: <https://github.com/madscheme/fastapi>
> - 장별 예제: [`example/`](https://github.com/madscheme/fastapi/tree/main/example) (파일명 = 예제 번호, 예: `8-14.py` = 예제 8-14)
> - 완성 프로젝트: [`src/`](https://github.com/madscheme/fastapi/tree/main/src)

---

## 0. Part 3 개요

### 무엇을 만드는가
**크립티드(cryptid, 상상 속 생물)** 와 그것을 찾는 **탐험가(explorer)** 정보를 관리하는 중간 규모 웹 서비스.

### 3계층 + 공통 컴포넌트

```
  Client (브라우저 / HTTPie / Postman)
        │  HTTP
        ▼
┌────────────────┐
│   Web 계층      │  web/       ← FastAPI 라우터, HTTP 입출력, 상태코드
├────────────────┤
│  Service 계층   │  service/   ← 비즈니스 로직 (사이트의 "심장")
├────────────────┤
│   Data 계층     │  data/      ← DB 접근 (SQLite, DB-API)
└────────────────┘
   공통: model/ (Pydantic 모델) · fake/ (가짜 데이터) · test/ (테스트) · error.py (예외)
```

### 설계 시 던지는 질문 (강의 도입용)
- 각 계층에는 무엇이 들어가야 하나? 계층 사이에는 무엇이 오가나?
- 나중에 코드를 바꿔도 다른 부분이 깨지지 않을까?
- 문제가 생기면 어떻게 찾고 고칠까?
- 보안은? 확장성과 성능은?
- 이 모든 것을 단순하게 유지할 수 있을까?

### 장별 구성과 권장 시간

| 장 | 주제 | 핵심 키워드 | 권장 시간 |
|---|---|---|---|
| 8 | Web 계층 | REST 설계, 디렉터리 구조, `APIRouter`, Fake 데이터, `/docs` | 3h |
| 9 | Service 계층 | 계층 분리, pass-through, 첫 pytest | 1.5h |
| 10 | Data 계층 | DB-API, SQLite, 환경변수 설정, 사용자 정의 예외 | 3h |
| 11 | 인증과 인가 | HTTP Basic, 비밀번호 해시, OAuth2, JWT, RBAC, CORS | 3h |
| 12 | 테스트 | 테스트 피라미드, mock vs fake, 계층별 단위 테스트, Schemathesis | 2.5h |
| 13 | 프로덕션 | Gunicorn/Uvicorn 워커, HTTPS, Docker, 성능, 트러블슈팅 | 1.5h |

### 전체 학습 흐름 — "위에서 아래로(Top-down)"

```
8장: Web 함수 안에 가짜 데이터  →  9장: Service로 이동  →  10장: Data 계층 + 실제 DB
                     (각 단계마다 엔드포인트는 계속 동작해야 함)
```

---

## 8장. Web 계층

### 학습 목표
- RESTful API의 구성 요소와 URL·메서드 설계 규칙을 설명할 수 있다.
- 계층별 디렉터리 구조를 만들고 `APIRouter`로 라우터를 분리할 수 있다.
- Pydantic 모델과 가짜(fake) 데이터로 CRUD 엔드포인트를 먼저 완성할 수 있다.

### 8.1 설계 접근법: Top-down? Bottom-up? Middle-out?

| 출발점 | 언제 적합한가 |
|---|---|
| **Data 계층부터** (Bottom-up) | 이미 데이터가 쌓인 DB가 있고, 이를 공개하고 싶을 때 |
| **Service 계층부터** (Middle-out) | 도메인 주도 설계(DDD) — 핵심 엔티티·모델부터 정의 |
| **Web 계층부터** (Top-down) | 인터페이스를 먼저 다듬고, 하위 계층은 가짜로 대체 |

- 이 책은 **Web 우선(Top-down)** 방식. FastAPI 자체를 익히려는 학습자에게 적합.
- 참고 키워드: 헥사고날 아키텍처, 포트와 어댑터.
- 참고 도서: *Clean Architectures in Python*, *Architecture Patterns with Python*, *Microservice APIs*.
- Web 계층은 사용자와 서비스를 잇는 **여러 방법 중 하나**일 뿐 (CLI, SDK도 가능). 다른 프레임워크에서는 view / presentation 계층이라 부름.

### 8.2 RESTful API 설계

**구성 요소**: 리소스(Resource) · ID · URL · 동사(HTTP 메서드)

| 메서드 | 의미 |
|---|---|
| `GET` | 리소스 조회 |
| `POST` | 새 리소스 생성 |
| `PUT` | 리소스 **전체** 교체 |
| `PATCH` | 리소스 **일부** 수정 |
| `DELETE` | 리소스 삭제 |

**URL 패턴**
- `verb /resource/` → 해당 타입의 **모든** 리소스에 적용
- `verb /resource/id` → 특정 ID의 리소스에 적용
- 정렬·페이지네이션 등 부가 옵션은 보통 **쿼리 파라미터**(`?sort=country`), 큰 데이터는 **HTTP body**

> **토론 포인트 — 단수 vs 복수 리소스 이름**
> 일반적인 REST 권고는 복수형(`/explorers`)이지만, 저자는 **단수형(`/explorer`)** 을 사용.
> 이유: `series`, `fish`처럼 단·복수가 같은 단어, `people`·`children` 같은 불규칙 복수, 변환 코드 필요 등.
> → 팀 컨벤션으로 정하면 된다는 점을 강조.

### 8.3 디렉터리 구조

```
fastapi/
└── src/
    ├── main.py          # 앱 진입점
    ├── web/             # FastAPI 웹 계층
    ├── service/         # 비즈니스 로직
    ├── data/            # 저장소 인터페이스
    ├── model/           # Pydantic 모델
    └── fake/            # 초기 가짜(stub) 데이터
   (각 디렉터리: __init__.py, creature.py, explorer.py)
```

- `__init__.py` : 디렉터리를 **패키지**로 인식시키는 빈 파일
- `PYTHONPATH` 설정으로 `src`를 import 기준 경로로 지정

```bash
# macOS / Linux
export PYTHONPATH=$PWD/src
```
```powershell
# Windows PowerShell
$env:PYTHONPATH = "$PWD\src"
```

### 8.4 첫 번째 웹사이트 코드

- `main.py`에서 `FastAPI()` 객체를 만들고 `uvicorn.run("main:app", reload=True)`로 실행
  - `"main:app"` = `main.py` 파일의 `app` 객체
  - `reload=True` = 코드 변경 시 자동 재시작
- 경로 파라미터 엔드포인트 추가: `@app.get("/echo/{thing}")`
- 소스: [`8-1.py`](https://github.com/madscheme/fastapi/blob/main/example/8-1.py), [`8-4.py`](https://github.com/madscheme/fastapi/blob/main/example/8-4.py)

**실습 확인**
```bash
http localhost:8000
http -b localhost:8000/echo/argh
```

### 8.5 요청(Request) 데이터의 위치

FastAPI의 **의존성 주입**으로 데이터가 HTTP 메시지의 어디에 있는지 선언:

| 위치 | 설명 |
|---|---|
| Header | HTTP 헤더 |
| Path | URL 경로 |
| Query | URL의 `?` 뒤 |
| Body | HTTP 본문 |
| (간접) | 환경 변수, 설정 파일 |

### 8.6 다중 라우터 — `APIRouter`

리소스별로 파일을 나누고 `prefix`로 URL을 묶은 뒤, `main.py`에서 `include_router()`로 연결.

```python
# web/explorer.py
router = APIRouter(prefix="/explorer")

# main.py
app.include_router(explorer.router)
app.include_router(creature.router)
```
- 소스: [`8-7.py`](https://github.com/madscheme/fastapi/blob/main/example/8-7.py), [`8-8.py`](https://github.com/madscheme/fastapi/blob/main/example/8-8.py)

### 8.7 Web 계층 구축 단계

1. **데이터 모델 정의** (`model/`) — Pydantic `BaseModel`
   - `Explorer`: name, country, description
   - `Creature`: name, country, area, description, aka
   - country는 ISO 2자리 국가 코드 사용
   - 소스: [`model/explorer.py`](https://github.com/madscheme/fastapi/blob/main/src/model/explorer.py), [`model/creature.py`](https://github.com/madscheme/fastapi/blob/main/src/model/creature.py)

2. **Stub과 Fake의 차이**

   | 용어 | 의미 |
   |---|---|
   | Stub (mock data) | 실제 모듈 호출 없이 반환되는 고정된 결과 |
   | Fake | 실제 데이터 소스의 일부 기능을 흉내 내는 대체물 (예: 메모리 DB) |

3. **공통 함수 설계 (CRUD 확장)** — `get_all` / `get_one` / `create` / `modify`(부분) / `replace`(전체) / `delete`
   - U(Update)를 modify와 replace로 분리한 것이 특징

4. **가짜 데이터 모듈** (`fake/`) — 리스트에 샘플 객체를 두고 CRUD 함수 제공
   - 소스: [`fake/explorer.py`](https://github.com/madscheme/fastapi/blob/main/src/fake/explorer.py), [`fake/creature.py`](https://github.com/madscheme/fastapi/blob/main/src/fake/creature.py)
   - 클래스 대신 **모듈 함수**로 구현 — 모듈 자체가 네임스페이스 역할

5. **Web 엔드포인트 연결** — 핵심 트릭
   ```python
   import fake.explorer as service   # 나중에 진짜 service로 교체할 자리
   ```
   → import 한 줄만 바꾸면 하위 계층을 교체할 수 있도록 설계
   - 소스: [`8-14.py`](https://github.com/madscheme/fastapi/blob/main/example/8-14.py) (explorer), [`8-15.py`](https://github.com/madscheme/fastapi/blob/main/example/8-15.py) (creature)

### 8.8 테스트

- **수동 테스트** (HTTPie): `GET`, `PUT`, `PATCH`, `DELETE` 각각 호출
- **자동 문서 / 테스트 폼**: `http://localhost:8000/docs` (Swagger UI), `/redoc`
  - 엔드포인트 펼치기 → *Try it out* → *Execute* → Response body 확인
  - 9장·10장 끝에서도 같은 테스트를 반복해 "데이터 파이프라인이 끊기지 않았는지" 확인

### 8.9 계층 간 대화 원칙

- Web 계층이 데이터가 필요하면 **반드시 Service 계층을 거친다.**
  - Web은 웹만, Data는 외부 저장소만 담당 → 세부 사항 분리
  - 계층을 **독립적으로 테스트** 가능
- 아주 작은 사이트라면 Service 계층은 생략 가능하지만 **Web과 Data는 반드시 분리**.

### 8.10 페이지네이션과 정렬

| 기능 | 예시 |
|---|---|
| 정렬 | `GET /explorer?sort=country` |
| 페이지네이션 | `GET /explorer?offset=10&size=10` |
| 둘 다 | `GET /explorer?sort=country&offset=10&size=10` |

- 파라미터를 Pydantic 모델로 정의하고 `Depends`로 주입하면 깔끔
- 실제 처리는 **Data 계층(DB)** 에서 하는 것이 효율적 (구현은 17장)

### 정리 & 확인 질문
- Top-down 방식에서 fake 모듈을 쓰는 이유는?
- `PUT`과 `PATCH`의 차이는? 둘 다 꼭 필요한가?
- `import fake.explorer as service` 패턴이 주는 이점은?

---

## 9장. Service 계층

### 학습 목표
- Service 계층의 역할과 "새지 않는(leak-free)" 계층 설계를 설명할 수 있다.
- Service 모듈을 추가하고 pytest로 첫 자동화 테스트를 작성할 수 있다.

### 9.1 Service 계층이란
- 사이트의 **심장이자 존재 이유** — 여러 소스의 요청을 받아 데이터(사이트의 DNA)에 접근하고 응답을 반환
- 공통 패턴: 생성 / 조회 / (부분·전체) 변경 / 삭제 × 하나 / 여러 개
- 향후 확장 리소스 예: 장소(Places), 이벤트(탐험, 목격 기록)

### 9.2 레이아웃
```
main.py
web/      service/      data/      model/      fake/      test/
(각각 __init__.py, creature.py, explorer.py)
```

### 9.3 보호(Protection)
- 계층의 장점: 모든 것을 한꺼번에 걱정하지 않아도 됨
- Service는 **데이터의 입출력**에만 집중, 인증·인가는 상위 계층(Web)이 처리 (11장)

### 9.4 Service 함수
- 지금은 거의 **pass-through(통과)** 계층 — 그래도 처음부터 구조를 갖추면 나중에 이득
- creature와 explorer를 한 파일로 합치고 싶지만, 결국 언젠가 다르게 처리해야 하므로 분리 유지
- `import fake.creature as data` → 10장에서 진짜 data 모듈로 교체
- 반환 타입 `Creature | None`은 Python 3.10+ 문법 (이전 버전은 `Optional[Creature]`)
- 소스: [`9-1.py`](https://github.com/madscheme/fastapi/blob/main/example/9-1.py), [`9-2.py`](https://github.com/madscheme/fastapi/blob/main/example/9-2.py) / 완성본 [`service/creature.py`](https://github.com/madscheme/fastapi/blob/main/src/service/creature.py)

### 9.5 테스트 디렉터리 구조

```
test/
├── unit/        # 한 계층 안의 함수 단위 (계층 경계를 넘지 않음)
│   ├── web/
│   ├── service/
│   └── data/
└── full/        # end-to-end (= contract test), 모든 계층을 관통
```
- pytest는 `test_` 접두사 / `_test` 접미사 파일을 자동 탐색

**API 설계 결정: 못 찾았을 때 무엇을 반환할까?**

| 선택지 | 비고 |
|---|---|
| `None` 반환 | 9장의 선택 — "없음"의 의미 그대로 |
| `TypeError` / `ValueError` | 내장 예외 중 가장 가깝지만 딱 맞지는 않음 |
| 사용자 정의 예외 (`Missing`) | **10장에서 이 방식으로 전환** |

- 소스: [`9-3.py`](https://github.com/madscheme/fastapi/blob/main/example/9-3.py) → 실행: `pytest -v test/unit/service/test_creature.py`

### 9.6 그 밖의 Service 수준 관심사

| 항목 | 설명 | 도구 |
|---|---|---|
| 로깅 | FastAPI는 호출마다 시간·메서드·URL 기록 (body/header는 X) | — |
| 메트릭·모니터링·관찰성 | 어떤 엔드포인트에 몇 명이 접근하는지 | Prometheus(수집), Grafana(시각화) |
| 트레이싱 | 요청의 각 단계별 소요 시간 측정 → 병목 찾기 | OpenTelemetry (Jaeger 계승) |

- 도메인 확장 아이디어: 탐험가↔생물 연결, 목격 데이터, 탐험, 사진·동영상, 굿즈 판매 → Part 4에서 일부 구현

### 정리 & 확인 질문
- 지금은 pass-through인데 왜 Service 계층을 미리 만드는가?
- 인증 처리를 Service가 아닌 Web 계층에서 하는 이유는?

---

## 10장. Data 계층

### 학습 목표
- Python DB-API의 핵심 함수와 파라미터 스타일을 설명할 수 있다.
- SQLite로 영속 데이터 계층을 만들고 3계층을 완전히 연결할 수 있다.
- 사용자 정의 예외로 계층 간 오류를 깔끔하게 전달할 수 있다.

### 10.1 DB-API (PEP 249)

**핵심 흐름**
```
conn = connect(...)  →  curs = conn.cursor()  →  curs.execute(stmt, params)  →  fetch...
```

| 실행 함수 | 용도 |
|---|---|
| `execute(stmt)` | 파라미터 없음 |
| `execute(stmt, params)` | 시퀀스(튜플/리스트) 또는 dict 파라미터 |
| `executemany(stmt, params_seq)` | 여러 파라미터 묶음 |

| 조회 함수 | 반환 |
|---|---|
| `fetchone()` | 튜플 하나 또는 `None` |
| `fetchall()` | 튜플 시퀀스 |
| `fetchmany(num)` | 최대 num개 튜플 |

**파라미터 스타일 5가지** (드라이버마다 지원 다름)

| 스타일 | SQL 부분 | 파라미터 |
|---|---|---|
| qmark | `name=?` | 튜플 |
| numeric | `name=:0` | 튜플 |
| format | `name=%s` | 튜플 |
| **named** | `name=:name` | dict ← **이 책에서 사용** |
| pyformat | `name=%(name)s` | dict |

> 강의 팁: 파라미터 바인딩은 **SQL 인젝션 방지**의 기본이라는 점을 함께 강조.

### 10.2 SQLite
- Python 표준 라이브러리 `sqlite3`에 포함
- **별도 서버 없음** — 라이브러리 + 단일 파일 저장
- 모델 ↔ DB 변환 유틸리티 2개
  - `row_to_model()` : fetch 결과 튜플 → Pydantic 모델
  - `model_to_dict()` : 모델 → named 파라미터용 dict
- 소스: [`10-2.py`](https://github.com/madscheme/fastapi/blob/main/example/10-2.py)

### 10.3 데이터의 이동 경로 정리
1. 8장: fake creatures/explorers → Web
2. 9장: fake → Service
3. **10장: Data 계층 + 실제 SQLite 파일(`cryptid.db`)** — 더 이상 가짜가 아님

### 10.4 DB 설정을 어떻게 전달할까?

| 방법 | 평가 |
|---|---|
| 코드에 하드코딩 | 간단하지만 유연성 없음 |
| 계층을 따라 위에서 아래로 전달 | ❌ 계층 분리 위반 (Web·Service가 DB 내부를 알게 됨) |
| **환경 변수** / 설정 파일 | ✅ Twelve-Factor App 권장, 테스트 DB 분리에도 유용 |

- 환경 변수 `CRYPTID_SQLITE_DB` (기본값 `db/cryptid.db`)
- 공통 초기화 모듈 `data/init.py` — **모듈은 싱글턴**이라 여러 번 import해도 한 번만 실행
- 테이블 생성: `create table if not exists ...`, `name text primary key` (인덱스로 테이블 풀스캔 방지)
- 소스: [`data/init.py`](https://github.com/madscheme/fastapi/blob/main/src/data/init.py), [`data/creature.py`](https://github.com/madscheme/fastapi/blob/main/src/data/creature.py), [`data/explorer.py`](https://github.com/madscheme/fastapi/blob/main/src/data/explorer.py)

### 10.5 Full 테스트에서 만난 문제들 (강의에서 재현하기 좋음)

| 증상 | 원인 | 해결 |
|---|---|---|
| `GET /explorer` → **405** | 라우트는 `/explorer/`(끝 슬래시)만 정의됨 | 경로 데코레이터를 `""`와 `"/"` 두 개 붙임 ([`10-7.py`](https://github.com/madscheme/fastapi/blob/main/example/10-7.py)) |
| `POST` → **422** | 필드명 오타(`contry`) → Pydantic이 Web 계층에서 검증 실패 | 오류 JSON의 `loc`로 위치 확인 |
| 생성 성공 → **201** | 리소스 생성의 관례적 상태 코드 | — |
| 같은 이름 재생성 → **500** | `sqlite3.IntegrityError`가 Web까지 그대로 올라옴 | 아래 예외 설계 |
| 없는 이름 조회 → **500** | `fetchone()`이 `None` → 언패킹 `TypeError` | 아래 예외 설계 |

### 10.6 계층을 지키는 오류 처리 설계

| 방안 | 단점 |
|---|---|
| DB 예외를 Web에서 직접 처리 | Web이 특정 DB를 알게 됨 → 계층 혼합 |
| 모든 함수가 `Model \| None` 반환 | 실패 이유를 알 수 없고 수정량이 많음 |
| **애플리케이션 예외 `Missing`, `Duplicate` 정의** | ✅ 선택 — DB에 독립적, Service 수정 없이 위로 전파 |

```
Data 계층: IntegrityError → raise Duplicate / 결과 없음 → raise Missing
   ↓ (Service는 수정 없음 — 예외는 그대로 위로 흐름)
Web 계층:  except Missing → HTTPException(404) / except Duplicate → HTTPException(409)
```
- 소스: [`error.py`](https://github.com/madscheme/fastapi/blob/main/src/error.py), [`10-18.py`](https://github.com/madscheme/fastapi/blob/main/example/10-18.py) (data), [`10-19.py`](https://github.com/madscheme/fastapi/blob/main/example/10-19.py) (web)
- `curs.rowcount`로 update/delete 대상이 실제로 있었는지 확인

### 10.7 Data 계층 단위 테스트
- import 전에 `os.environ["CRYPTID_SQLITE_DB"] = ":memory:"` → **메모리 DB**로 실제 파일을 건드리지 않음
- pytest **fixture** `sample()`로 매 테스트마다 새 `Creature` 제공
  - fixture scope: function(기본, 매번) / session(한 번)
- `pytest.raises(Duplicate)`, `pytest.raises(Missing)`로 예외 발생 검증
- 소스: [`10-22.py`](https://github.com/madscheme/fastapi/blob/main/example/10-22.py) / [`test/unit/data/`](https://github.com/madscheme/fastapi/tree/main/src/test/unit/data)

**권장 테스트 순서**: 코드 작성 중 수동 테스트 → 문법 오류 수정 후 단위 테스트 → 전 계층 연결 후 Full 테스트

### 정리 & 확인 질문
- DB 접속 정보를 계층을 따라 내려보내면 안 되는 이유는?
- `IntegrityError`를 `Duplicate`로 바꿔 던지면 무엇이 좋아지는가?
- `:memory:` DB를 테스트에 쓰는 장점은?

---

## 11장. 인증(Authentication)과 인가(Authorization)

### 학습 목표
- 인증과 인가의 차이를 설명하고, 주요 인증 방식을 비교할 수 있다.
- OAuth2 Password 흐름 + JWT로 사용자 인증을 계층별로 구현할 수 있다.
- 인가 모델(Admin, ACL, RBAC)과 미들웨어·CORS를 이해한다.

### 11.1 핵심 개념

| 용어 | 질문 |
|---|---|
| **인증 (authn)** | 당신은 누구인가? (Who) |
| **인가 (authz)** | 무엇을 할 수 있는가? (What) |

- 정말 인증이 필요한가? → 완전 익명은 DoS 등에 취약, 방문자 분석(고유 방문자, 인기 페이지 등)에도 인증이 필요
- 인증을 쓴다면 **반드시 HTTPS** (13장)

### 11.2 인증 방식

| 방식 | 설명 |
|---|---|
| 사용자명/이메일 + 비밀번호 | HTTP Basic / Digest 인증 |
| API 키 | 불투명한 긴 문자열 + 비밀값 |
| OAuth2 | 인증·인가 표준 모음 |
| JWT | 서명된 사용자 정보를 담은 인코딩 형식 |

### 11.3 전역 인증: 공유 비밀 (HTTP Basic)
- `HTTPBasic()` + `Depends`로 사용자명/비밀번호 수신
- 서버에 저장된 값과 다르면 `HTTPException(401)` (공식 이름은 Unauthorized, 실제 의미는 *unauthenticated*)
- `fastapi.status.HTTP_401_UNAUTHORIZED` 상수 사용 권장
- 한계: 개인 식별 불가, 비밀이 새면 끝
- 소스: [`11-1.py`](https://github.com/madscheme/fastapi/blob/main/example/11-1.py), [`11-4.py`](https://github.com/madscheme/fastapi/blob/main/example/11-4.py)

```bash
http -a newphone:whodis? localhost:8000/who
```

### 11.4 개별 사용자 인증에 필요한 것
1. 사용자 정보를 HTTP 헤더로 전달 + **HTTPS**
2. 비밀번호는 **해시**로 변환 (역산 불가)
3. DB의 User 테이블에는 **해시만 저장** (평문 절대 금지)
4. 입력 비밀번호를 해시해 DB 해시와 비교
5. 일치 시 User 객체를 위로 전달, 불일치 시 `None` 또는 예외

### 11.5 OAuth2 + JWT 구현 (Bottom-up으로 진행)

**필요 패키지 (원서 기준)**
```bash
pip install "python-jose[cryptography]"   # JWT
pip install passlib                       # 비밀번호 해시 (bcrypt)
pip install python-multipart              # 폼 처리
```

| 계층 | 파일 | 핵심 내용 |
|---|---|---|
| Model | [`model/user.py`](https://github.com/madscheme/fastapi/blob/main/src/model/user.py) | `User(name, hash)` — 평문 비밀번호 없음 |
| Data | [`data/user.py`](https://github.com/madscheme/fastapi/blob/main/src/data/user.py) | `user`(활성) + `xuser`(삭제됨) 테이블 |
| Fake | [`fake/user.py`](https://github.com/madscheme/fastapi/blob/main/src/fake/user.py) | DB 없이 테스트용 사용자 |
| Service | [`service/user.py`](https://github.com/madscheme/fastapi/blob/main/src/service/user.py) | 해시·검증, JWT 생성·해독, `auth_user()` |
| Web | [`web/user.py`](https://github.com/madscheme/fastapi/blob/main/src/web/user.py) | `OAuth2PasswordBearer`, `POST /user/token` |
| Top | [`main.py`](https://github.com/madscheme/fastapi/blob/main/src/main.py) | `include_router(user.router)` |

> **설계 포인트 — 삭제 사용자 처리**
> 흔히 `deleted` 불리언 컬럼을 두지만, 저자는 삭제된 사용자를 **별도 `xuser` 테이블로 이동**.
> → 모든 쿼리마다 `deleted` 검사를 반복하지 않아도 되고, 카디널리티 낮은 컬럼 인덱스 문제도 회피.

**Service 계층 주요 함수**

| 함수 | 역할 |
|---|---|
| `get_hash(plain)` | 평문 → bcrypt 해시 |
| `verify_password(plain, hash)` | 평문을 해시해 비교 |
| `auth_user(name, plain)` | 사용자 조회 + 비밀번호 검증 |
| `create_access_token(data, expires)` | `exp`(만료) 포함 JWT 생성 (기본 15분) |
| `get_jwt_username(token)` | JWT 해독 → `sub`(사용자명) |
| `get_current_user(token)` | 토큰 → User 객체 |

- 환경 변수 `CRYPTID_UNIT_TEST`가 있으면 `fake.user`, 없으면 `data.user`를 import — **실행 시점에 가짜/진짜 교체**
- `SECRET_KEY`는 운영 환경에서 반드시 변경 (환경 변수로 관리 권장)

### 11.6 인증 흐름 요약

```
1. 클라이언트 → POST /user/token (username, password 폼)
2. 서버: 비밀번호 해시 비교 → 일치하면 JWT 액세스 토큰 발급
3. 이후 요청: Authorization: Bearer <JWT> 헤더로 전송
4. 서버: JWT 해독 → 사용자명 획득 (DB 재조회 불필요)
5. 인증된 사용자로 메트릭 수집, 사용자별 정보 저장 등
```

### 11.7 JWT
- 인증 방식이 아니라 **인코딩 형식** (RFC 7519)
- `Header.Payload.Signature` — 점(.)으로 구분된 3부분, 각각 Base64 URL 인코딩된 JSON
- URL·헤더·쿠키 어디든 전달 가능
- 장점: DB 조회 불필요 / 단점: **토큰 폐기(revoke)를 직접 감지할 수 없음**
- 실습: <https://jwt.io> 에서 토큰 디코딩해 보기

### 11.8 서드파티 인증: OIDC
- "Google로 로그인" 등 — OAuth2 위에 구축된 **OpenID Connect**
- 액세스 토큰 + **ID 토큰** 발급
- FastAPI 공식 문서엔 예제가 없으므로 서드파티 패키지 활용

### 11.9 인가 모델의 단계적 발전

| 상황 | 테이블 설계 |
|---|---|
| 관리자만 추적, 나머지는 익명 | `Admin` 테이블 |
| 전원 인증 + 일부 엔드포인트는 관리자만 | `User` 인증 후 `Admin` 확인 |
| 여러 권한(읽기/쓰기 등) | `Permission` + `UserPermission` → **ACL** |
| 권한 조합이 복잡 | `Role` + `UserRole` → **RBAC** |

- 원칙: **쓰기 권한은 읽기 권한보다 엄격하게**

### 11.10 미들웨어와 CORS
- **미들웨어**: 요청을 가로채 처리 → 경로 함수 전달 → 응답을 가로채 처리 → 반환 (데코레이터와 유사)
  - 전역 관심사(CORS 등)는 미들웨어, 엔드포인트별은 `Depends`
- **CORS**: 출처(Origin = 프로토콜 + 도메인 + 포트)가 다른 프론트엔드의 접근 허용 범위 지정
  - `CORSMiddleware`에 `allow_origins`, `allow_methods`, `allow_headers`, `allow_credentials` 설정
  - 소스: [`11-13.py`](https://github.com/madscheme/fastapi/blob/main/example/11-13.py)

### 11.11 서드파티 패키지
FastAPI Users, FastAPI JWT Auth, FastAPI-Login, AuthX, fastapi-sso, Fief 등 — 직접 구현 전에 검토 (유지보수 여부 확인 필수)

### 정리 & 확인 질문
- 401과 403의 차이는?
- 비밀번호를 암호화가 아니라 **해시**로 저장하는 이유는?
- JWT의 "DB 조회 불필요"라는 장점이 동시에 단점이 되는 상황은?

---

## 12장. 테스트

### 학습 목표
- 단위·통합·전체 테스트의 범위와 테스트 피라미드를 설명할 수 있다.
- mock(구조적 테스트)과 fake/double(행위적 테스트)의 차이를 비교할 수 있다.
- 계층별 단위 테스트와 Schemathesis 속성 기반 테스트를 실행할 수 있다.

### 12.1 테스트 도구
- 수동: HTTPie, Requests, HTTPX, 브라우저, curl, httpbin, **Postman**, Chrome DevTools
- 수동 테스트의 한계 → 나중 변경이 이전 기능을 깨는 **회귀(regression)** → **자동화 테스트** 필요

### 12.2 어디서 / 무엇을 테스트할까

```
        /\        Full (적게)       — 전체 API와 하위 스택
       /  \       Integration       — 계층 간 연결
      /____\      Unit (많이)       — 한 계층 안의 개별 함수
```

**확인할 입력 유형**: 누락 · 중복 · 잘못된 타입 · 잘못된 순서 · 유효하지 않은 값 · 거대한 입출력

| 오류 발생 위치 | 예 |
|---|---|
| Web | Pydantic 모델 불일치 → 422 |
| Data | 누락·중복 데이터, SQL 문법 오류, 큰 결과의 타임아웃·메모리 부족 |
| 모든 계층 | 일반 버그 |

### 12.3 pytest
```bash
pip install pytest pytest-mock
```
- **테스트 자동 탐색**: `test_` 접두사/`_test` 접미사, 하위 디렉터리까지
- **assert 실패 상세 출력**: 기대값 vs 실제값
- **fixture**: 테스트 데이터·DB 초기화 주입 (FastAPI의 의존성 주입과 유사)
- **parametrize**: 여러 데이터로 반복 실행

**레이아웃**
```
test/
├── unit/{web, service, data}
├── integration/
└── full/
```

### 12.4 단위 테스트의 격리: Mock vs Double(Fake)

| 구분 | Mock | Double / Fake |
|---|---|---|
| 방식 | `unittest.mock.patch("mod1.preamble", return_value="")` | 환경 변수로 가짜 모듈을 import |
| 테스트 성격 | **구조적** — 내부 모듈·변수 이름을 알아야 함 | **행위적** — 내부 구조를 몰라도 됨 |
| 비용 | 함수마다 mock 작성 | 코드에 환경 변수 분기 추가 |

- mock 작성법 4가지: `with` 컨텍스트 매니저 / `as`로 객체 받기 / 데코레이터 / 별도로 `return_value` 지정
- 소스: [`12-1.py`](https://github.com/madscheme/fastapi/blob/main/example/12-1.py) ~ [`12-9.py`](https://github.com/madscheme/fastapi/blob/main/example/12-9.py)
- 이 책은 **import 교체(double) 방식**을 채택 — 앞서 만든 `fake/` 패키지와 자연스럽게 연결

```python
if os.getenv("CRYPTID_UNIT_TEST"):
    from fake import creature as service
else:
    from service import creature as service
```

### 12.5 계층별 단위 테스트

| 계층 | 격리 방법 | 검증 내용 | 소스 |
|---|---|---|---|
| **Web** | `CRYPTID_UNIT_TEST` → fake service | 엔드포인트 존재, 파라미터, 상태 코드, `HTTPException` | [`test/unit/web/test_creature.py`](https://github.com/madscheme/fastapi/blob/main/src/test/unit/web/test_creature.py) |
| **Service** | `CRYPTID_UNIT_TEST` → fake data | CRUD 결과, `Missing`/`Duplicate` 전파 (예외는 잡지 않고 Web에 맡김) | [`test/unit/service/test_creature.py`](https://github.com/madscheme/fastapi/blob/main/src/test/unit/service/test_creature.py) |
| **Data** | `CRYPTID_SQLITE_DB=":memory:"` | 함수 + SQL 쿼리 자체 | [`test/unit/data/test_creature.py`](https://github.com/madscheme/fastapi/blob/main/src/test/unit/data/test_creature.py) |

- fixture: `sample()` (새 객체), `fakes()` (기존 가짜 목록)

### 12.6 통합 테스트
- A→B→C 파이프라인이면 A→B, B→C, A→C … 조합이 폭증
- 현실적 대안: **전체 테스트 + 마지막 저장소만 대체**
  - 메모리 SQLite / pgmock(PostgreSQL) / Mongomock / Pytest Mock Resources(Docker)
  - 또는 운영과 같은 종류의 테스트 DB를 환경 변수로 지정

**Repository 패턴** (책에서 구현하지 않음, 개념 소개)
- 메모리 저장소가 중간에서 실제 DB 백엔드와 연결
- **Unit of Work** 패턴과 함께 — 여러 작업을 한 번에 커밋 또는 롤백

### 12.7 전체(Full) 테스트
- 방법 1: HTTP로 실제 서버 호출 (HTTPie, Requests)
- 방법 2: FastAPI/Starlette **`TestClient`** — TCP 연결 없이 직접 호출
- 소스: [`test/full/`](https://github.com/madscheme/fastapi/tree/main/src/test/full)

**속성 기반 테스트 — Schemathesis**
```bash
pip install hypothesis schemathesis
schemathesis run http://localhost:8000/openapi.json
```
- FastAPI가 자동 생성한 **OpenAPI 스키마**를 읽어 수많은 입력값을 자동 생성해 공격
- 책의 실행 결과: 12개 엔드포인트 중 PATCH 2개에서 실패 발견
- 핵심 메시지: **타입 힌트 → OpenAPI 스키마 → 자동 문서 + 자동 테스트**

> 강의 연계: Postman에서 `openapi.json`을 import해 컬렉션을 만들고 테스트 스크립트를 붙이는 실습도 가능.

### 12.8 보안 테스트 · 부하 테스트
- **보안**: Schemathesis의 인증 관련 속성 기반 테스트 문서 참고
- **부하**: **Locust** — 순수 Python 스크립트로 수십만 사용자 시뮬레이션
  - `pip install locust`, 확장: `locust-grasshopper` (여러 HTTP 호출에 걸친 시간 측정)
  - 측정 대상: API 호출, DB 읽기/쓰기, 메모리, 디스크, 네트워크 지연·대역폭

### 정리 & 확인 질문
- mock 기반 테스트가 "구조적"이라는 말의 의미와 단점은?
- Data 계층 테스트에는 왜 fake 모듈이 필요 없는가?
- Schemathesis가 테스트 케이스를 직접 작성하지 않아도 되는 이유는?

---

## 13장. 프로덕션

### 학습 목표
- 다중 워커, 리버스 프록시, HTTPS, 컨테이너 등 배포 구성 요소를 설명할 수 있다.
- 성능 개선 기법과 트러블슈팅 순서를 이해한다.

### 13.1 배포에 필요한 것
지금까지는 `localhost:8000`의 Uvicorn 하나. 운영에서는:
- 서버 프로세스 유지 (**supervisor**)
- 외부 요청 수집·분배 (**리버스 프록시**)
- 응답 반환
- **HTTPS 종료** (SSL 복호화)

### 13.2 다중 워커

```bash
# 권장: Gunicorn이 Uvicorn 워커를 관리 (프로세스 관리 포함)
pip install "uvicorn[standard]" gunicorn
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
```bash
# Uvicorn 단독 다중 워커 (프로세스 관리 기능은 약함)
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```
- Gunicorn은 WSGI 서버지만 Uvicorn 워커 클래스로 ASGI(FastAPI) 실행 가능
- 워커 4~12개면 초당 수백~수천 요청 처리 가능 (Gunicorn 문서)

### 13.3 HTTPS
- FastAPI 공식 HTTPS 문서 + **Traefik**(리버스 프록시·로드밸런서 + 자동 HTTPS)
- 인증서: 무료 **Let's Encrypt**

### 13.4 Docker · 클라우드 · Kubernetes
- **Docker**: VM보다 가볍고 빠른 컨테이너, 클라우드 배포의 사실상 표준
  ```dockerfile
  FROM python:3.12
  WORKDIR /code
  COPY ./requirements.txt /code/requirements.txt
  RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
  COPY ./src /code/src
  CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
  ```
  (원서는 FastAPI 공식 문서의 Dockerfile을 인용 — 프로젝트 구조에 맞게 경로 조정)
- **클라우드**: Linode, Heroku 등 배포 튜토리얼 참고
- **Kubernetes**: "어떻게"가 아니라 "무엇을 원하는지" 선언 → 서비스 유지, 트래픽 급증 시 자동 확장

### 13.5 성능

| 기법 | 요점 |
|---|---|
| **async** | I/O 대기가 많은 코드는 `async def` → 대기 중 다른 요청 처리 (Flask·Django 대비 벤치마크 우위의 이유) |
| **캐시** | 잘 바뀌지 않는 데이터는 `functools.cache()` / `lru_cache()` |
| **DB 인덱스** | 느린 사이트의 가장 흔한 원인 = 인덱스 누락. `WHERE` 절 컬럼은 인덱스 |
| **배치·스트리밍** | 연속 쿼리는 묶고, 큰 파일은 스트리밍 |
| **작업 큐** | 이메일 발송·이미지 변환 등 오래 걸리는 작업은 **Celery** 등으로 위임 |
| **Python 자체** | PyPy, C/C++/Rust 확장, Cython, (신규) Mojo |

- 성능의 두 측면: **단일 요청 처리 시간** vs **동시 처리 요청 수**

### 13.6 트러블슈팅
- 문제가 발생한 지점에서 **아래 방향(bottom-up)** 으로 추적

| 상태 코드 | 1차 의심 대상 |
|---|---|
| 401 / 403 / 404 | 인증·인가 문제 또는 리소스 없음 |
| **422** | 대부분 Pydantic 모델 검증 실패 |
| **500** | FastAPI 뒤의 서비스(DB 등) 실패 |

- **로깅**: Uvicorn은 stdout에 메서드·URL 기록 (body·헤더·쿠키는 X) → 같은 입력으로 재현 → Web/Service/Data 함수에 `print()` 추가
- 예외를 던질 때 **입력값과 구체적 오류를 메시지에 포함**
- **메트릭**: Prometheus(수집) + Grafana(시각화) + OpenTelemetry(타이밍)
  - Service 메트릭은 비즈니스 관점, Web/Data 메트릭은 기술 관점

### 정리 & 확인 질문
- Gunicorn + Uvicorn 워커 조합을 쓰는 이유는?
- 잘 되던 서비스가 데이터가 늘자 갑자기 느려졌다. 가장 먼저 무엇을 확인할까?

---

## 부록 A. 강의 시 주의할 점 (원서 코드 vs 최신 환경)

원서는 2023년 기준이라 그대로 실행하면 오류가 나는 부분이 있습니다. 시연 전 확인하세요.

| 항목 | 원서 | 현재 권장 / 비고 |
|---|---|---|
| Pydantic 모델 → dict | `model.dict()` | Pydantic v2: `model.model_dump()` (`.dict()`는 deprecated) |
| JWT 라이브러리 | `python-jose` | FastAPI 공식 문서는 현재 **`PyJWT`** 사용 |
| 비밀번호 해시 | `passlib` + bcrypt | FastAPI 공식 문서는 현재 **`pwdlib`**(Argon2) 사용. passlib은 최신 bcrypt와 호환 경고 발생 |
| 현재 시각 | `datetime.utcnow()` | Python 3.12+ deprecated → `datetime.now(timezone.utc)` |
| Duplicate 상태 코드 | 10장 예제는 `404` | **`409 Conflict`** 가 적절 (12장·`web/user.py`는 409 사용) |
| `row_to_model` | `Creature(name, description, ...)` 위치 인자 | Pydantic 모델은 **키워드 인자** 필요: `Creature(name=name, ...)` |
| 9장 예제 import | `from models.creature ...` | 디렉터리명은 `model` (오타) |
| 13장 "404 = 인증 오류" | 원문 표기 | 인증 실패는 **401**, 권한 부족은 **403**, 404는 리소스 없음 |
| SQLite 커밋 | 예제에 `conn.commit()` 없음 | 프로세스 간 영속성이 필요하면 `commit()` 또는 `isolation_level=None` 확인 |
| Windows 환경 변수 | `export PYTHONPATH=...` | PowerShell: `$env:PYTHONPATH = "$PWD\src"` |
| Schemathesis 실행 | `schemathesis <url>` | 최신 버전: `schemathesis run <url>` |

> 수업에서는 저장소의 [`src/`](https://github.com/madscheme/fastapi/tree/main/src) 완성본을 기준으로 하되, 위 항목을 "버그 찾기" 실습 소재로 활용하는 것도 좋습니다.

---

## 부록 B. 실습 과제 제안

1. **[8장]** `fake/explorer.py`의 `create`/`delete`가 실제로 리스트를 수정하도록 바꾸고 `/docs`에서 확인하기
2. **[8장]** `Depends`와 Pydantic 모델로 `?sort=&offset=&size=` 페이지네이션 파라미터 받기
3. **[10장]** `data/explorer.py`를 참고해 `test/unit/data/test_explorer.py` 직접 작성하기
4. **[10장]** `PUT`(replace)을 실제 SQL로 구현하고 Full 테스트로 검증하기
5. **[11장]** `get_current_user`를 `Depends`로 연결해 `POST /creature`를 로그인 사용자만 호출하도록 보호하기
6. **[11장]** `User` 모델에 `is_admin` 필드를 추가해 관리자만 `DELETE` 가능하게 만들기 (간단한 인가)
7. **[12장]** `TestClient`로 `/explorer` 엔드포인트 Full 테스트 작성 → Schemathesis로 PATCH 실패 원인 찾아 고치기
8. **[13장]** 프로젝트를 Dockerfile로 이미지화하고 Gunicorn + Uvicorn 워커 4개로 실행하기

---

## 부록 C. 예제 번호 ↔ 소스 파일 빠른 참조

| 장 | 예제 파일 (`example/`) | 완성본 (`src/`) |
|---|---|---|
| 8 | `8-1`, `8-4`, `8-7`, `8-8`, `8-10`~`8-15` | `main.py`, `web/`, `model/`, `fake/` |
| 9 | `9-1`, `9-2`, `9-3` | `service/`, `test/unit/service/` |
| 10 | `10-2`~`10-5`, `10-7`, `10-16`~`10-19`, `10-22` | `data/`, `error.py`, `test/unit/data/`, `test/full/` |
| 11 | `11-1`, `11-4`, `11-7`~`11-13` | `model/user.py`, `data/user.py`, `fake/user.py`, `service/user.py`, `web/user.py` |
| 12 | `12-1`~`12-3`, `12-5`, `12-7`~`12-9`, `12-11`~`12-16` | `test/unit/{web,service,data}/`, `test/full/` |
| 13 | (코드 예제 없음 — 명령어 위주) | — |

예제 폴더: <https://github.com/madscheme/fastapi/tree/main/example>
