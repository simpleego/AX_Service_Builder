# 처음으로 시작하는 FastAPI — Part 4. 갤러리 (강의자료)

> 원서: Bill Lubanovic, *FastAPI: Modern Python Web Development* (O'Reilly) — 14장 ~ 18장
> 예제 소스: <https://github.com/madscheme/fastapi>
> - 장별 예제: [`example/`](https://github.com/madscheme/fastapi/tree/main/example) (파일명 = 예제 번호, 예: `15-4.py` = 예제 15-4)
> - 완성 프로젝트: [`src/`](https://github.com/madscheme/fastapi/tree/main/src)
> - 선수 학습: Part 3 (Web · Service · Data 3계층 사이트)

---

## 0. Part 4 개요

### 무엇을 하는가
Part 3에서 만든 **크립티드 웹사이트**를 기반으로, 웹에서 흔히 하는 작업들을 FastAPI로 하나씩 붙여 보는 **응용 예제 모음(갤러리)**.

```
                 Part 3에서 만든 3계층 사이트 (web / service / data)
                                   │
   ┌──────────────┬────────────────┼────────────────┬──────────────┐
   ▼              ▼                ▼                ▼              ▼
 14장 DB·AI     15장 파일        16장 폼·템플릿    17장 시각화      18장 게임
 (DB 선택지,    (업로드/다운로드, (Form, Jinja2)   (차트, 지도)    (Wordle형,
  부하 테스트,   정적 파일)                                         JS + AJAX)
  LLM 엔드포인트)
```

### 장별 구성과 권장 시간

| 장 | 주제 | 핵심 키워드 | 권장 시간 |
|---|---|---|---|
| 14 | 데이터베이스, 데이터 과학, 약간의 AI | SQL/NoSQL 비교, SQLAlchemy, SQLModel, Faker 부하 테스트, Hugging Face | 2.5h |
| 15 | 파일 | `File()`, `UploadFile`, `FileResponse`, `StreamingResponse`, `StaticFiles` | 1.5h |
| 16 | 폼과 템플릿 | `Form()`, GET vs POST 폼, `Jinja2Templates` | 1.5h |
| 17 | 데이터 탐색과 시각화 | csv, tabulate, pandas, Plotly 차트·지도, 이미지 `Response` | 2h |
| 18 | 게임 | 무상태(stateless) 웹의 상태 관리, Jinja + JS `fetch()`, 점수 로직, parametrize | 2.5h |

### Part 4 전체에서 강조할 메시지
- FastAPI는 이름에 "API"가 있지만 **파일, HTML 폼, 템플릿, 이미지, 대화형 페이지**도 제공할 수 있다.
- 새 기능을 붙일 때도 **Part 3의 계층 구조(Web → Service → Data)** 를 그대로 따른다 (특히 18장).

---

## 14장. 데이터베이스, 데이터 과학, 약간의 AI

### 학습 목표
- 관계형 DB와 NoSQL DB의 특징과 대표 제품, Python 드라이버를 비교할 수 있다.
- SQLAlchemy의 계층(Core / Expression Language / ORM)과 SQLModel을 설명할 수 있다.
- Faker로 대량 데이터를 만들어 계층별 성능을 측정할 수 있다.
- Hugging Face 모델을 FastAPI 엔드포인트로 감쌀 수 있다.

### 14.1 "데이터베이스"라는 말의 세 가지 의미
1. 서버 종류 (PostgreSQL, SQLite, MySQL …)
2. 실행 중인 서버 인스턴스
3. 서버 안의 테이블 묶음

→ 수업에서 어떤 의미로 쓰는지 구분해 말하기.

**DB가 대신 해결해 주는 문제**: 동시 접근 · 인덱싱 · 데이터 일관성

### 14.2 관계형 DB와 Python 드라이버

| 구분 | DB | Python 드라이버 |
|---|---|---|
| 오픈소스 | SQLite | `sqlite3` (표준 라이브러리) |
| | PostgreSQL | `psycopg2`, `asyncpg` |
| | MySQL | `MySQLdb`, `PyMySQL` |
| 상용 | Oracle | `python-oracledb` |
| | SQL Server | `pyodbc`, `pymssql` |
| | IBM Db2 | `ibm_db` |

**SQL 관련 상위 패키지**

| 패키지 | 특징 |
|---|---|
| **SQLAlchemy** | 가장 인기 있는 SQL 패키지, 여러 수준으로 사용 가능 |
| **SQLModel** | SQLAlchemy + Pydantic, **FastAPI 제작자**가 만듦 |
| Records | Requests 제작자의 간단한 쿼리 API |

### 14.3 SQLAlchemy의 계층 (아래에서 위로)

```
 ORM                    ← 도메인 모델(클래스)로 쿼리. 가장 추상적, 학습 비용 큼
 Expression Language    ← Table, Column, select(), insert() 등 파이썬 메서드로 SQL 표현
 Core                   ← Engine(DB-API 구현), 접속 URL, 커넥션 풀, 트랜잭션, SQL 방언 처리, 직접 SQL
```

- **Core**: 여러 DB 종류를 다룰 때 방언(dialect) 처리 덕분에 강력
- **Expression Language**: ORM은 아니지만 DB 종류와 무관하게 쿼리 작성. SQL이 어렵다면 고려
- **ORM**: 객체지향을 선호하는 개발자에게 인기. 단, 새로운 추상화를 하나 더 배워야 함
- 소스: [`14-1.py`](https://github.com/madscheme/fastapi/blob/main/example/14-1.py) (순수 SQL), [`14-2.py`](https://github.com/madscheme/fastapi/blob/main/example/14-2.py) (Expression Language)

> **토론 포인트 — 저자의 관점**
> 많은 FastAPI 책이 DB 장에서 바로 ORM으로 들어가지만, 저자는 **"먼저 SQL로, SQL이 복잡해지면 Expression Language나 ORM으로"** 를 권장.
> 추상화가 깨질 때 문제가 두 배가 되기 때문. → ORM 우선 vs SQL 우선, 학생들과 장단점 토론.

**SQLModel**: SQLAlchemy ORM + Pydantic 데이터 정의·검증 → 하나의 클래스로 DB 테이블과 API 모델을 겸함

### 14.4 관계형 DB 이모저모
- **SQLite**: 퍼블릭 도메인, 모든 브라우저와 스마트폰에 탑재된 가장 널리 배포된 소프트웨어 중 하나
- **PostgreSQL**: Ingres의 후계, 오늘날 오픈소스 개발자의 1순위 선택
- **EdgeDB**: asyncio 제작자가 만든 "Post-SQL / graph-relational" DB
  - 내부적으로 PostgreSQL 사용, 쿼리 언어 **EdgeQL**은 SQL로 번역되어 실행
  - SQL의 약점인 **조합성 부족**(쿼리 중첩이 어려움)을 해결하려는 시도

### 14.5 NoSQL 데이터베이스

| DB | 특징 | Python 드라이버 |
|---|---|---|
| **Redis** | 메모리 기반 데이터 구조 서버, Python 자료구조와 유사 | `redis-py` |
| **MongoDB** | 컬렉션(=테이블), 문서(=행), **고정 스키마 없음**, 문서 = 파이썬 dict | `PyMongo`, `Motor` |
| **Cassandra** | 수백 노드로 분산되는 대규모 DB (Java). 호환 대안: ScyllaDB (C++) | DataStax Driver |
| **Elasticsearch** | DB라기보다 인덱스, 전문(full-text) 검색에 주로 사용 | Python Elasticsearch Client |

- NoSQL = "No SQL" 또는 "Not only SQL"
- 관계형: **정규화**(셀 하나에 값 하나 등 규칙) / NoSQL: 규칙 완화, JSON처럼 들쭉날쭉한 구조, **비정규화**(문서에 필요한 데이터를 모두 포함)

### 14.6 SQL DB의 NoSQL 기능
- 최근 SQL 표준은 **JSON 저장·검색·인덱싱**을 지원 (SQLite, PostgreSQL, MySQL, Oracle 등)
- SQL + JSON = 두 세계의 장점: 외래 키·보조 인덱스 같은 SQL 기능 + 유연한 구조
- 결론: 데이터가 사각형 테이블에 맞지 않으면 → NoSQL DB / JSON 지원 관계형 DB / Post-SQL DB 중 선택

### 14.7 데이터베이스 부하 테스트 — Faker
- **Faker**: 이름, 국가 등 가짜 데이터를 대량으로 빠르게 생성
- 예제: 탐험가 10만 명 생성 → SQLite에 적재 → 읽기 시간 측정
- 소스: [`14-3.py`](https://github.com/madscheme/fastapi/blob/main/example/14-3.py)

**측정 결과 (원서)**

| 측정 항목 | 시간 |
|---|---|
| 쓰기 (10만 행, 한 건씩) | 약 14.9초 |
| Data 계층 읽기 (`get_all()`) | 약 0.4초 |
| API 읽기 (`TestClient`로 `GET /explorer/`) | 약 2.6초 |

**결과 해석 (강의 핵심)**
- API 읽기가 DB 읽기보다 훨씬 느림 → FastAPI의 **JSON 변환 오버헤드**
- 쓰기가 느린 이유 → `create()`만 있고 `create_many()`가 없어 한 건씩 저장
  - 대량 적재가 필요하면 **새 Data 함수 + 권한이 제한된 Web 엔드포인트** 추가
- 10만 행을 한 번에 아무에게나 반환하면 안 됨 → **페이지네이션** 또는 CSV 다운로드 제공
- `read_db()`를 두 번 호출하는 이유: 첫 호출의 시작 비용을 빼고 공정하게 비교하기 위해

### 14.8 데이터 과학과 AI
- Python은 데이터 과학·머신러닝의 대표 언어 (데이터 가공에 강함)
- **pandas**: SQL로 하기 까다로운 데이터 조작
- **PyTorch**: 대표 ML 도구 (계산은 C/C++, 상위 데이터 통합은 Python)
- **Chroma**: SQLite처럼 쓰는 ML/LLM용 데이터베이스 (벡터 DB)

> **용어 주의 — "모델"**
> Pydantic의 모델 = 관련 데이터 필드를 묶은 Python 클래스
> AI의 모델 = 데이터에서 패턴을 찾는 다양한 기법의 산물

### 14.9 실습: Hugging Face LLM을 FastAPI로 감싸기

```bash
pip install torch torchvision
pip install transformers
```

- 모델: `google/flan-t5-base` (중간 크기 오픈소스 모델)
- 흐름: 모델·토크나이저 로드(앱 시작 시 1회) → `GET /ai?line=질문` → 토큰화 → `generate()` → 디코딩 → 문자열 반환
- 소스: [`14-5.py`](https://github.com/madscheme/fastapi/blob/main/example/14-5.py)

```bash
uvicorn ai:app
http -b localhost:8000/ai line=="What are you?"     # HTTPie에서 쿼리 파라미터는 ==
```

- 작은 모델이라 엉뚱한 답이 나옴 → **환각(hallucination)** 개념 소개
- 더 큰 모델(`google/flan-t5-xl`)은 답이 나아지지만 다운로드와 응답이 느림

> 강의 연계: 같은 엔드포인트를 Claude 등 상용 LLM API 호출로 바꿔 보는 실습으로 확장 가능.

### 정리 & 확인 질문
- ORM을 바로 쓰지 않고 SQL부터 시작하라는 저자의 근거는?
- MongoDB의 "고정 스키마 없음"은 장점이자 단점이다. 각각 어떤 상황인가?
- 부하 테스트에서 API 읽기가 DB 읽기보다 6배 이상 느린 이유는? 어떻게 개선할까?

---

## 15장. 파일

### 학습 목표
- 작은 파일과 큰 파일의 업로드·다운로드 방식을 구분해 구현할 수 있다.
- `StaticFiles`로 디렉터리를 전통적인 웹 서버처럼 제공할 수 있다.

### 15.1 준비
```bash
pip install python-multipart   # 파일·폼 처리
pip install aiofiles           # 비동기 파일 I/O
```
- 파일 업로드는 JSON이 아니라 **폼(multipart) 형식**으로 전송됨

### 15.2 업로드: `File()` vs `UploadFile`

| 구분 | `File()` | `UploadFile` |
|---|---|---|
| 용도 | **작은** 파일 | **큰** 파일 |
| 타입 | `bytes` (메모리에 전체 조립) | `SpooledTemporaryFile` (주로 디스크) |
| 선언 | `small_file: bytes = File()` (괄호 필요) | `big_file: UploadFile` |
| 제공 정보 | 바이트 내용 | `.filename`, `.size`, `read()`/`write()`/`seek()` |
| 권장 함수 | `async def` (업로드 중 서버를 막지 않음) | `async def` |

- 소스: [`15-1.py`](https://github.com/madscheme/fastapi/blob/main/example/15-1.py) (`POST /small`), [`15-4.py`](https://github.com/madscheme/fastapi/blob/main/example/15-4.py) (`POST /big`)

**테스트**
```bash
http -f -b POST http://localhost:8000/small small_file@1KB.bin
http -f -b POST http://localhost:8000/big big_file@1GB.bin
```
- `-f` : 폼 형식으로 전송 (JSON 아님)
- `small_file@1KB.bin` : `small_file` = 경로 함수의 매개변수 이름, `@` = 파일 첨부, `1KB.bin` = 올릴 파일
- 테스트용 파일은 직접 만들 수 있음 (Linux/macOS: `head -c 1000 /dev/urandom > 1KB.bin`, Windows: `fsutil file createnew 1KB.bin 1000`)

### 15.3 다운로드: `FileResponse` vs `StreamingResponse`

| 구분 | `FileResponse` | `StreamingResponse` |
|---|---|---|
| 용도 | 작은 파일, 한 번에 전송 | 큰 파일, **청크(조각) 단위** 전송 |
| 사용법 | `return FileResponse(경로)` | 제너레이터를 `content`로 전달 |

- 소스: [`15-7.py`](https://github.com/madscheme/fastapi/blob/main/example/15-7.py) (`FileResponse`), [`15-10.py`](https://github.com/madscheme/fastapi/blob/main/example/15-10.py) (`StreamingResponse`)
- 확인: `http -b http://localhost:8000/small/1KB.bin | wc -c` → 1000

> **보안 주의 (강의에서 꼭 언급)**
> 예제처럼 URL의 파일 이름을 그대로 `FileResponse(name)`에 넘기면, `../` 등을 이용해 **서버의 다른 파일을 내려받는 경로 탐색(path traversal) 공격**에 노출될 수 있다.
> 운영 코드에서는 허용된 디렉터리 안의 파일인지 반드시 검사할 것.

### 15.4 정적 파일 제공 — `StaticFiles`
- `app.mount("/static", StaticFiles(directory=..., html=True), name="free")`
  - `/static`으로 시작하는 URL → `static/` 디렉터리의 파일 반환
  - `Path(__file__).resolve().parent`로 `main.py`와 같은 위치 기준 경로 계산
  - `html=True` : 디렉터리 요청 시 `index.html`을 자동 반환 (전통적인 웹 서버처럼 동작)
  - 하위 디렉터리도 깊이 제한 없이 제공
- 소스: [`15-12.py`](https://github.com/madscheme/fastapi/blob/main/example/15-12.py) / 정적 파일 예시: [`src/static/`](https://github.com/madscheme/fastapi/tree/main/src/static)

```bash
http -b localhost:8000/static/abc.txt    # → abc :)
http -b localhost:8000/static/           # → index.html 내용
```

### 정리 & 확인 질문
- 1GB 파일 업로드에 `File()`을 쓰면 어떤 문제가 생기나?
- 파일 업로드·다운로드 경로 함수를 `async def`로 만드는 이유는?
- `app.mount()`와 `app.include_router()`의 차이는?

---

## 16장. 폼과 템플릿

### 학습 목표
- `Form()`으로 HTML 폼 데이터를 받고, GET 폼과 POST 폼의 차이를 설명할 수 있다.
- Jinja2 템플릿으로 서버 데이터를 HTML에 넣어 응답할 수 있다.

### 16.1 폼(Form)
- FastAPI의 기본 입력은 JSON이지만, `Path`·`Query`처럼 **`Form` 의존성**으로 폼 데이터를 받을 수 있음
- `python-multipart` 필요, 15장의 `static/` 디렉터리에 테스트용 HTML 폼을 둠

```python
@app.post("/who2")
def greet3(name: str = Form()):
    return f"Hello, {name}?"
```

**GET 폼에서 생긴 함정 (강의에서 재현하기 좋음)**

| 시도 | 결과 |
|---|---|
| HTTPie: `http -f -b GET localhost:8000/who2 name="Bob Frapples"` | 정상 동작 |
| 브라우저: `form1.html` (`method="get"`) 제출 | **422** — `body.name` 필드 없음 |

- 원인: HTML 폼은 **GET이면 입력값을 쿼리 문자열**(`/who2?name=...`)로 보냄 → 본문(body)의 Form을 기대한 FastAPI가 422 반환
  - 게다가 URL에 원래 있던 쿼리 파라미터는 지워지고 폼 값으로 대체됨
- 해결: 폼은 **`method="post"`** 로 전송 → `@app.post` 엔드포인트로 받기
- 교훈: **HTML 파일에서 폼을 제출할 때는 POST를 사용**
- 소스: [`16-1.py`](https://github.com/madscheme/fastapi/blob/main/example/16-1.py) (GET), [`16-4.py`](https://github.com/madscheme/fastapi/blob/main/example/16-4.py) (POST) / 폼 HTML: [`static/form1.html`](https://github.com/madscheme/fastapi/blob/main/src/static/form1.html), [`static/form2.html`](https://github.com/madscheme/fastapi/blob/main/src/static/form2.html)

### 16.2 템플릿(Template)
- 비유: **매드 립스(Mad Libs)** — 빈칸이 있는 글에 단어를 채워 넣는 게임
- 템플릿 = 서버가 데이터를 채워 넣을 **빈칸이 있는 HTML** (15장의 정적 HTML과 대비)
- FastAPI는 Flask에서 익숙한 **Jinja(Jinja2)** 를 지원

**Jinja 문법 핵심**

| 문법 | 의미 |
|---|---|
| `{{ 변수 }}` | 값 출력 |
| `{% for ... %}` … `{% endfor %}` | 반복 |
| `{% if ... %}` … `{% endif %}` | 조건 |

**구성 방법**
1. `main.py` 옆에 `template/` 디렉터리 생성, 그 안에 `list.html` 작성
2. `Jinja2Templates(directory=...)` 객체 생성
3. 경로 함수에서 `TemplateResponse("list.html", {"request": request, "creatures": ..., "explorers": ...})` 반환
   - `request` 객체를 반드시 함께 넘겨야 함
4. 브라우저로 `http://localhost:8000/list` → 생물·탐험가 표가 HTML로 출력

- 소스: [`16-6.template`](https://github.com/madscheme/fastapi/blob/main/example/16-6.template) (템플릿), [`16-7.py`](https://github.com/madscheme/fastapi/blob/main/example/16-7.py) (설정) / 완성본: [`src/template/list.html`](https://github.com/madscheme/fastapi/blob/main/src/template/list.html)

> 강의 팁: 템플릿은 `{{ }}` 출력 시 HTML을 **자동 이스케이프**하므로 XSS를 기본적으로 막아 준다는 점도 함께 설명.

### 정리 & 확인 질문
- 같은 요청이 HTTPie에서는 되고 브라우저 폼에서는 422가 난 이유는?
- 정적 파일(15장)과 템플릿(16장)은 각각 언제 쓰는가?
- API(JSON) 서버와 템플릿(HTML) 서버를 하나의 FastAPI 앱에 함께 둘 때의 장단점은?

---

## 17장. 데이터 탐색과 시각화

### 학습 목표
- 구분자 파일을 csv · tabulate · pandas로 읽고 출력할 수 있다.
- Plotly로 차트와 지도를 만들어 FastAPI 엔드포인트에서 **이미지로 반환**할 수 있다.

### 17.1 Python과 데이터
- Python의 인기 이유: 쉬운 학습, 깔끔한 문법, 풍부한 표준 라이브러리, 많은 서드파티 패키지, **데이터 가공에 강함**
- 전통적인 ETL 작업, 최근에는 AI 모델용 데이터 준비에도 핵심
- 커뮤니티: **PyData**

### 17.2 데이터 원본: PSV 파일
- 크립티드 데이터는 **파이프(`|`) 구분 파일**로 제공
  - 저장소: [`src/db/creature.psv`](https://github.com/madscheme/fastapi/blob/main/src/db/creature.psv), [`src/db/explorer.psv`](https://github.com/madscheme/fastapi/blob/main/src/db/explorer.psv), SQLite: [`src/db/cryptid.db`](https://github.com/madscheme/fastapi/blob/main/src/db/cryptid.db)
- 왜 파이프인가? CSV의 쉼표는 데이터 안에도 자주 등장하고, TSV의 탭은 공백과 구분이 어려움
- 필드: `name` · `country` (`*` = 여러 나라) · `area` (선택, 미국 주 코드 등) · `description` · `aka`

### 17.3 텍스트로 읽고 출력하기

| 도구 | 특징 | 반환 | 소스 |
|---|---|---|---|
| `csv` (표준) | `csv.reader(file, delimiter="\|")`, `DictReader`도 있음 | 리스트 | [`17-1.py`](https://github.com/madscheme/fastapi/blob/main/example/17-1.py) |
| `tabulate` | 표 형태로 보기 좋게 출력 (`pip install tabulate`) | 문자열 | [`17-3.py`](https://github.com/madscheme/fastapi/blob/main/example/17-3.py) |
| `pandas` | `read_csv(fname, sep="\|")`, 강력한 데이터 가공 | **DataFrame** | [`17-5.py`](https://github.com/madscheme/fastapi/blob/main/example/17-5.py) |

```bash
python load_csv.py creature.psv
python load_pandas.py creature.psv
```

### 17.4 웹으로 출력하기 — 기존 계층 재사용
- 이제부터는 SQLite DB의 데이터를 Part 3의 **`service.get_all()` → `data.get_all()`** 로 가져와 가공
- 이미 있는 `GET /creature` 엔드포인트가 전체 데이터를 반환함을 먼저 확인

### 17.5 차트·그래프 패키지

| 패키지 | 특징 |
|---|---|
| Matplotlib | 기능이 매우 많지만 보기 좋게 만들려면 손이 많이 감 |
| **Plotly** | 대화형 그래프 중심, 적은 코드로 보기 좋은 결과 ← **이 책의 선택** |
| Dash | Plotly 기반 대시보드 |
| Seaborn | Matplotlib 기반 상위 인터페이스, 그래프 종류는 적음 |
| Bokeh | JavaScript 연동, 대용량 데이터 대시보드 |

- 선택 기준: 그래프 종류 · 스타일 · 사용 편의성 · 성능 · 데이터 한계
- Plotly 구성: Plotly Express(간단) / Plotly(메인) / Dash(앱)

```bash
pip install plotly
pip install kaleido     # 그림을 이미지 파일(PNG)로 내보내기
```

### 17.6 FastAPI에서 이미지를 반환하는 패턴 (핵심)

```python
fig_bytes = fig.to_image(format="png")
return Response(content=fig_bytes, media_type="image/png")
```
- Plotly 문서의 `fig.show()` 대신, 이미지 **바이트**를 만들어 `Response`로 직접 반환
- `media_type`으로 브라우저가 이미지로 인식하게 함

### 17.7 차트 예제

| 엔드포인트 | 내용 | 소스 |
|---|---|---|
| `GET /creature/test` | Plotly 내장 iris 데이터 산점도 — 설치 확인용 | [`17-8.py`](https://github.com/madscheme/fastapi/blob/main/example/17-8.py) |
| `GET /creature/plot` | 생물 이름 **첫 글자별 개수** 막대그래프 (`collections.Counter`) | [`17-9.py`](https://github.com/madscheme/fastapi/blob/main/example/17-9.py) |

- 브라우저 주소창에 `localhost:8000/creature/plot` 입력 → PNG 이미지 표시

### 17.8 지도 패키지와 지도 예제
- 검색 팁: "Python map"은 딕셔너리 결과가 나오므로 GIS, geo, cartography, spatial 등으로 검색
- 대표 패키지: PyGIS, PySAL, Cartopy, **Folium**(JS 연동), Google Maps 클라이언트, Geemap, Geoplot, **GeoPandas**, ArcGIS/ArcPy
- 지도 종류: 단계 구분도(choropleth), 벡터, 래스터

**예제: 크립티드가 사는 나라 지도** (`GET /creature/map`)
1. 모든 생물의 `country`(ISO **2자리** 코드)를 집합으로 수집
2. Plotly의 `choropleth`는 ISO **3자리** 코드를 요구 → `country_converter`로 변환
   ```bash
   pip install country_converter
   ```
3. `px.choropleth(locationmode="ISO-3", locations=iso3_codes)` → PNG로 반환
- 소스: [`17-10.py`](https://github.com/madscheme/fastapi/blob/main/example/17-10.py)
- 확장 과제: `country == "US"`인 생물의 `area`(주 코드)로 `locationmode="USA-states"` 미국 지도 만들기

### 정리 & 확인 질문
- PSV 형식을 쓴 이유는?
- 차트를 `fig.show()`가 아니라 `Response`로 반환하는 이유는?
- 데이터의 국가 코드 형식과 라이브러리가 요구하는 형식이 다를 때 어떤 선택지가 있나?

---

## 18장. 게임

### 학습 목표
- 무상태(stateless)인 웹에서 여러 단계에 걸친 상호작용의 상태를 어디에 둘지 설계할 수 있다.
- Jinja 템플릿 + JavaScript `fetch()`로 클라이언트와 서버가 JSON을 주고받는 게임을 구현할 수 있다.
- 새 기능도 Web → Service → Data 계층으로 나누고 parametrize로 테스트할 수 있다.

### 18.1 Python 게임 패키지 (참고)
- 텍스트: Adventurelib
- 그래픽: PyGame, pyglet, Python Arcade, HARFANG, Panda3D
- 이 장에서는 사용하지 않음 — 웹사이트 구성이라는 목표에 집중하기 위해

### 18.2 게임 로직을 어디에 둘까? — 상태 관리

웹은 **무상태**: 서버는 매 요청마다 클라이언트를 처음 보는 것처럼 대함 → 단계 사이의 상태를 어딘가에 보관해야 함

| 방식 | 상태 위치 | 특징 |
|---|---|---|
| 클라이언트 중심 | 브라우저 (JavaScript) | JS를 잘 안다면 좋은 선택 |
| 서버 중심 | 서버 DB | 게임 ID를 발급하고 매 단계 ID와 함께 요청 |
| **균형형 (SPA 방식)** ← 이 책의 선택 | 일부는 클라이언트, 로직·데이터는 서버 | JS가 AJAX로 서버 호출, 페이지 일부만 갱신 |

### 18.3 게임 설계 — "Cryptonamicon" (Wordle 스타일)
- 정답은 `cryptid.db`에 있는 **크립티드 이름** 중 하나 (글자 수 = 이름 길이, 시도 횟수 제한 없음)

```
1. 브라우저 → GET /game
2. 서버: DB에서 무작위 생물 이름 선택 → Jinja 템플릿(HTML+CSS+JS)에 hidden 값으로 넣어 반환
3. 화면: 이름 글자 수만큼 입력 칸 표시
4. 사용자가 추측 입력 → JS fetch()로 POST /game {guess, word} (JSON)
5. 서버: 점수 계산 → "HCMM..." 같은 점수 문자열 반환
6. 화면: 글자마다 색칠 (H=초록 정답 위치 / C=노랑 다른 위치 / M=회색 없음)
7. 모두 초록이면 성공 😀, 아니면 4번부터 반복
```

- 점수 문자열의 각 글자(`H`/`C`/`M`)를 그대로 **CSS 클래스 이름**으로 사용 → JS 코드가 단순해짐
- 프레임워크(React 등) 없이 **순수(vanilla) JavaScript** 사용

### 18.4 Web 계층 — 라우팅 주의점
- `GET /creature/game`으로 만들면 안 되는 이유: 기존 `GET /creature/{name}`이 **먼저 매칭**되어 `name="game"`으로 처리됨
- 해결: 새 최상위 경로 **`/game`** 에 두 엔드포인트를 둠

| 엔드포인트 | 역할 |
|---|---|
| `GET /game` | 무작위 이름을 받아 `game.html` 템플릿 응답 (`request` 필수 전달) |
| `POST /game` | `word`, `guess`를 `Body()`로 받아 점수 반환 |

- `main.py`에 `app.include_router(game.router)` 추가
- 소스: [`18-1.py`](https://github.com/madscheme/fastapi/blob/main/example/18-1.py), [`18-2.py`](https://github.com/madscheme/fastapi/blob/main/example/18-2.py) / 완성본: [`src/web/game.py`](https://github.com/madscheme/fastapi/blob/main/src/web/game.py)

### 18.5 클라이언트 템플릿 (`template/game.html`)
- **CSS**: `.H`(초록) / `.C`(노랑) / `.M`(회색) 클래스
- **JavaScript**
  - `post_guess()`: 입력 칸들의 글자를 합쳐 `fetch()`로 `POST /game` (JSON 본문)
  - `show_score()`: 결과 표에 새 행을 추가하고 글자별로 CSS 클래스 지정, 정답이면 😀 표시
- **Jinja**: `{% for letter in word %}`로 글자 수만큼 입력 칸 생성, `{{word}}`를 hidden input에 저장
- 소스: [`18-3.template`](https://github.com/madscheme/fastapi/blob/main/example/18-3.template) / 완성본: [`src/template/game.html`](https://github.com/madscheme/fastapi/blob/main/src/template/game.html)

### 18.6 Service 계층 — 점수 계산 알고리즘
- `get_word()`: Data 계층으로 그대로 전달
- `get_score(actual, guess)`: Wordle 채점 로직
  1. 길이가 다르면 빈 문자열 반환
  2. **1차 순회**: 같은 위치의 같은 글자 → `H`
  3. **2차 순회**: `H`가 아닌 글자 중, 정답에 있고 **남은 개수 안에 드는** 글자 → `C`, 나머지는 `M`
  - `Counter`(정답의 글자별 개수)와 `defaultdict`(추측에서 사용한 개수)로 **중복 글자**를 올바르게 처리
- 소스: [`18-4.py`](https://github.com/madscheme/fastapi/blob/main/example/18-4.py), [`18-5.py`](https://github.com/madscheme/fastapi/blob/main/example/18-5.py) / 완성본: [`src/service/game.py`](https://github.com/madscheme/fastapi/blob/main/src/service/game.py)

> 강의 팁: 두 번 순회하는 이유(먼저 `H`를 확정해야 중복 글자의 `C` 판정이 정확해짐)를 화이트보드에서 예시로 풀어 보기.
> 예) 정답 `bigfoot`, 추측 `toofgib` → `CCCHCCC`

### 18.7 테스트 — `pytest.mark.parametrize`
- 반복문을 쓰지 않고 (입력, 기대값) 목록을 테스트 함수에 주입

| 추측 (정답: `bigfoot`) | 기대 점수 |
|---|---|
| `bigfoot` | `HHHHHHH` |
| `abcdefg` | `MCMMMCC` |
| `toofgib` | `CCCHCCC` |
| `wronglength` | `""` |
| `""` | `""` |

- 소스: [`18-6.py`](https://github.com/madscheme/fastapi/blob/main/example/18-6.py) / 완성본: [`src/test/unit/service/test_game.py`](https://github.com/madscheme/fastapi/blob/main/src/test/unit/service/test_game.py)

### 18.8 Data 계층
- `select name from creature order by random() limit 1` → 무작위 이름 하나
- 결과가 없으면 기본값 `"bigfoot"`
- 소스: [`18-7.py`](https://github.com/madscheme/fastapi/blob/main/example/18-7.py) / 완성본: [`src/data/game.py`](https://github.com/madscheme/fastapi/blob/main/src/data/game.py)

### 18.9 플레이
브라우저에서 `http://localhost:8000/game` 접속 → 글자 입력 → 제출 → 색깔 확인 → 정답까지 반복 (대소문자 섞어서 입력해 보기)

### 정리 & 확인 질문
- 일반적인 요청-응답 엔드포인트와 이 게임의 엔드포인트는 무엇이 다른가?
- `/creature/game` 경로를 쓰면 왜 동작하지 않는가?
- 정답 이름을 HTML hidden 값으로 클라이언트에 보내는 설계의 문제점은? (→ 개발자 도구로 정답이 보임. 서버 중심 상태 관리로 바꾸려면?)

---

## 부록 A. 강의 시 주의할 점 (원서 코드 vs 최신 환경)

원서는 2023년 기준이며 인쇄된 예제에 오타가 꽤 있습니다. 시연 전 확인하세요.

| 위치 | 원서 | 수정 / 비고 |
|---|---|---|
| 14-2 | `from sqlalchemy import Metadata, connect` | 클래스명은 `MetaData`, 연결은 `create_engine("sqlite:///cryptid.db")` 후 `engine.connect()`. `insert()`는 만들기만 하고 실행하지 않음 → `conn.execute(...)` 필요 |
| 14-3 | `description=f.description` | `f.text()` 등 메서드 호출이어야 함 |
| 14-5 | `generator_config=config` | `generation_config=config` |
| 14-5 | 모델 이름 `flan-75-xl` (본문) | `google/flan-t5-xl` |
| 15-10 | `from pathlib import path`, `gen_file(file_path=path)` | `Path`로 수정, 인자 이름 일치시키기. 또한 `file.read()`는 **파일 전체를 한 번에** 읽으므로 청크 단위로 `yield`하도록 고쳐야 스트리밍의 의미가 있음 |
| 15-11 | 테스트 URL `/big/1GB.bin` | 엔드포인트는 `/download_big/{name}` |
| 15-12 | `Path(__file__).resolve.parent` | `resolve()` — 괄호 누락 |
| 16-7 | `TemplateResponse("list.html", {"request": request, ...})` | 최신 Starlette: `TemplateResponse(request, "list.html", {...})` (구 방식은 경고 발생) |
| 16-7 | `from fake.creature import fakes` | Part 3의 fake 모듈 변수명(`_creatures` 등)과 맞추기 |
| 17-3 | `csv.reader` 사용 | `import csv` 누락 |
| 17-1 등 | 파일명 `cryptid.psv` | 저장소의 실제 파일은 `src/db/creature.psv` |
| 17-8~10 | `kaleido` | kaleido v1부터는 PC에 **Chrome**이 필요. 문제가 생기면 `pip install "kaleido<1"` 또는 Chrome 설치 |
| 17-9 | `px.histogram(x=..., y=dict)` | 글자별 개수를 이미 셌다면 `px.bar(x=letters, y=[counts.get(l, 0) for l in letters])`가 정확 |
| 17-10 | `service.get_all()` | 17-9에서는 `get_all`을 직접 import — 한 가지 방식으로 통일. 경로 함수 이름 `map`은 내장 함수를 가림 |
| 18-5 | `return ERROR` | `ERROR`가 정의되지 않음 → `return ""` |
| 18-5 | `HIT` 주석이 "다른 위치" | 주석이 `CLOSE`와 뒤바뀜 |
| 18-5 | 본문엔 "소문자로 변환"한다고 설명 | 코드엔 변환이 없음 → `actual = actual.lower(); guess = guess.lower()` 추가 |
| 18-3 | `fetch("http://localhost:8000/game")` | 절대 주소 대신 `"/game"`(상대 경로)이 배포에 유리 |
| 공통 | Pydantic `.dict()` | Pydantic v2: `.model_dump()` |

> 위 오류들은 그대로 **"버그 찾기" 실습 과제**로 활용하기 좋습니다. 저장소의 [`src/`](https://github.com/madscheme/fastapi/tree/main/src) 완성본은 일부가 수정되어 있으니 비교해 보세요.

---

## 부록 B. 실습 과제 제안

1. **[14장]** `data/explorer.py`에 `create_many()`(`executemany`)를 추가하고, Faker 10만 건 적재 시간을 한 건씩 저장한 것과 비교하기
2. **[14장]** `GET /explorer`에 `offset`/`size` 페이지네이션을 넣고, 부하 테스트의 API 읽기 시간 변화 측정하기
3. **[14장]** `/ai` 엔드포인트를 상용 LLM API 호출로 바꾸고, 응답 품질과 시간 비교하기
4. **[15장]** 업로드한 파일을 `uploads/` 디렉터리에 저장하고, 경로 탐색 공격(`../`)을 막는 다운로드 엔드포인트 만들기
5. **[16장]** 생물 등록 HTML 폼(`POST`) → `Form()`으로 받아 `service.create()` 호출 → 결과를 `list.html` 템플릿으로 보여 주기
6. **[17장]** `area` 필드로 미국 주별 크립티드 지도(`locationmode="USA-states"`) 만들기
7. **[17장]** 국가별 생물 수 막대그래프 엔드포인트 `GET /creature/by_country` 추가하기
8. **[18장]** 정답을 클라이언트에 보내지 않도록, 서버가 게임 ID를 발급하고 DB(또는 메모리)에 정답을 보관하는 방식으로 바꾸기
9. **[18장]** 시도 횟수를 6번으로 제한하고, 실패 시 정답을 공개하기

---

## 부록 C. 예제 번호 ↔ 소스 파일 빠른 참조

| 장 | 예제 파일 (`example/`) | 완성본 (`src/`) |
|---|---|---|
| 14 | `14-1`, `14-2`, `14-3`, `14-5` | (별도 스크립트) |
| 15 | `15-1`, `15-4`, `15-7`, `15-10`, `15-12` | `static/` |
| 16 | `16-1`, `16-4`, `16-6.template`, `16-7` | `static/form1.html`, `static/form2.html`, `template/list.html` |
| 17 | `17-1`, `17-3`, `17-5`, `17-8`, `17-9`, `17-10` | `db/creature.psv`, `db/cryptid.db`, `web/creature.py` |
| 18 | `18-1`, `18-2`, `18-3.template`, `18-4` ~ `18-7` | `web/game.py`, `service/game.py`, `data/game.py`, `template/game.html`, `test/unit/service/test_game.py` |

예제 폴더: <https://github.com/madscheme/fastapi/tree/main/example>

### 원서 부록 안내
- **부록 A (Further Reading)**: FastAPI 공식 문서·GitHub, 관련 도서·튜토리얼 목록
- **부록 B (Creatures and Humans)**: 예제에 쓰인 크립티드와 탐험가 목록 — 18장 게임의 "커닝 페이퍼"
