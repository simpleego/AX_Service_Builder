FastAPI를 처음 배우는 비전공자 기준으로 **설치 → 개발환경 → 실행 → 간단한 서버 코드 → 테스트** 순서로 정리하면 다음과 같습니다. Windows 11 + VS Code 환경을 기준으로 하겠습니다.

## 1. 프로젝트 폴더 만들기

예를 들어 VS Code에서 다음 폴더를 만듭니다.

```text
fastapi_exam/
```

VS Code 터미널에서 해당 폴더로 이동합니다.

```bash
cd fastapi_exam
```

---

## 2. 가상환경 만들기

프로젝트마다 사용하는 파이썬 패키지를 분리하기 위해 가상환경을 사용하는 것을 권장합니다.

```bash
python -m venv venv
```

폴더 구조는 다음과 같이 됩니다.

```text
fastapi_exam/
└── venv/
```

### Windows에서 가상환경 실행

CMD라면:

```bash
venv\Scripts\activate
```

PowerShell이라면:

```powershell
.\venv\Scripts\Activate.ps1
```

정상적으로 실행되면 터미널 앞에 다음처럼 표시됩니다.

```text
(venv) C:\fastapi_exam>
```

가상환경을 종료하려면:

```bash
deactivate
```

---

# 3. FastAPI 설치

가상환경이 활성화된 상태에서 설치합니다.

```bash
pip install fastapi uvicorn
```

두 패키지의 역할은 간단히 구분하면 다음과 같습니다.

| 패키지       | 역할                        |
| --------- | ------------------------- |
| `fastapi` | 웹 API 서버 프로그램 작성          |
| `uvicorn` | FastAPI 프로그램을 실제로 실행하는 서버 |

즉,

```text
FastAPI
   ↓
웹 애플리케이션 작성

Uvicorn
   ↓
FastAPI 애플리케이션 실행
```

설치 확인:

```bash
pip list
```

---

# 4. VS Code 개발환경

VS Code에서는 다음 정도만 준비하면 충분합니다.

추천 확장 프로그램:

```text
Python
Pylance
```

그리고 `Ctrl + Shift + P`를 누른 후

```text
Python: Select Interpreter
```

를 선택하여 다음과 같은 가상환경 Python을 지정합니다.

```text
fastapi_exam\venv\Scripts\python.exe
```

이 부분이 중요합니다.

즉,

```text
VS Code
   ↓
현재 프로젝트의 venv
   ↓
FastAPI 설치 패키지 사용
```

---

# 5. 가장 간단한 FastAPI 서버

프로젝트 폴더에 다음 파일을 만듭니다.

```text
main.py
```

코드는 다음과 같습니다.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello FastAPI"}
```

전체 구조는 이제 다음과 같습니다.

```text
fastapi_exam/
│
├── venv/
│
└── main.py
```

---

# 6. 서버 실행

터미널에서 다음 명령을 실행합니다.

```bash
uvicorn main:app --reload
```

여기서

```text
main:app
```

의 의미가 중요합니다.

```text
main
 ↓
main.py

app
 ↓
app = FastAPI()
```

즉,

```python
main.py
```

안에 있는

```python
app = FastAPI()
```

객체를 실행한다는 뜻입니다.

`--reload`는 소스 코드를 수정하면 서버를 자동으로 다시 실행해 주는 개발용 옵션입니다.

---

# 7. 웹 브라우저에서 확인

서버를 실행하면 일반적으로 다음 주소가 나타납니다.

```text
http://127.0.0.1:8000
```

브라우저에서 접속하면:

```json
{
    "message": "Hello FastAPI"
}
```

가 출력됩니다.

---

# 8. FastAPI의 매우 중요한 기능: 자동 API 문서

FastAPI가 교육용으로도 편리한 이유 중 하나입니다.

다음 주소로 접속합니다.

```text
http://127.0.0.1:8000/docs
```

그러면 **Swagger UI**가 자동으로 생성됩니다.

여기에서 API를 직접 실행해 볼 수 있습니다.

또 다른 API 문서는:

```text
http://127.0.0.1:8000/redoc
```

입니다.

---

# 9. GET API 하나 더 만들기

다음과 같이 수정해 보겠습니다.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI 서버입니다."}


@app.get("/hello")
def hello():
    return {"message": "안녕하세요."}
```

브라우저에서

```text
http://127.0.0.1:8000/hello
```

접속하면:

```json
{
    "message": "안녕하세요."
}
```

가 출력됩니다.

---

# 10. URL에서 값 전달하기

FastAPI에서 가장 먼저 실습하기 좋은 기능입니다.

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "FastAPI 서버입니다."}


@app.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"{name}님 안녕하세요."
    }
```

다음 주소로 접속합니다.

```text
http://127.0.0.1:8000/hello/홍길동
```

결과:

```json
{
    "message": "홍길동님 안녕하세요."
}
```

여기서

```python
{name}
```

은 URL로부터 데이터를 받는 **Path Parameter**입니다.

---

# 11. 숫자를 전달받아 계산하기

```python
@app.get("/square/{number}")
def square(number: int):
    return {
        "number": number,
        "result": number * number
    }
```

접속:

```text
http://127.0.0.1:8000/square/10
```

결과:

```json
{
    "number": 10,
    "result": 100
}
```

FastAPI는

```python
number: int
```

처럼 자료형을 지정하면 자동으로 타입 검사도 해줍니다.

---

# 12. Query Parameter 사용하기

URL을 다음처럼 사용하는 방식입니다.

```text
/add?a=10&b=20
```

코드:

```python
@app.get("/add")
def add(a: int, b: int):
    return {
        "a": a,
        "b": b,
        "result": a + b
    }
```

접속:

```text
http://127.0.0.1:8000/add?a=10&b=20
```

결과:

```json
{
    "a": 10,
    "b": 20,
    "result": 30
}
```

---

# 13. POST 방식의 가장 간단한 예제

실제 웹서비스에서는 데이터를 서버로 전달할 때 POST를 많이 사용합니다.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class User(BaseModel):
    name: str
    age: int


@app.post("/users")
def create_user(user: User):

    return {
        "name": user.name,
        "age": user.age,
        "message": "사용자가 등록되었습니다."
    }
```

POST는 브라우저 주소창에서 바로 테스트하기보다

```text
http://127.0.0.1:8000/docs
```

에서 테스트하면 편합니다.

예를 들어 JSON을 입력합니다.

```json
{
    "name": "홍길동",
    "age": 25
}
```

응답:

```json
{
    "name": "홍길동",
    "age": 25,
    "message": "사용자가 등록되었습니다."
}
```

---

# 14. 수업용으로는 이 코드 하나로 시작하면 좋습니다

초기 FastAPI 수업에서는 아래 정도면 충분합니다.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# 홈
@app.get("/")
def home():
    return {"message": "FastAPI Server"}


# Path Parameter
@app.get("/hello/{name}")
def hello(name: str):
    return {
        "message": f"{name}님 안녕하세요."
    }


# Query Parameter
@app.get("/add")
def add(a: int, b: int):
    return {
        "result": a + b
    }


# POST 데이터 구조
class User(BaseModel):
    name: str
    age: int


# POST
@app.post("/users")
def create_user(user: User):
    return {
        "name": user.name,
        "age": user.age
    }
```

실행:

```bash
uvicorn main:app --reload
```

API 문서:

```text
http://127.0.0.1:8000/docs
```

---

## 15. FastAPI의 전체 흐름을 이렇게 이해하면 쉽습니다

```text
웹 브라우저 / React
        │
        │ HTTP 요청
        ▼
   FastAPI 서버
        │
        ├── GET
        ├── POST
        ├── PUT
        └── DELETE
        │
        ▼
Python 프로그램
        │
        ▼
Database / AI / LLM
```

예를 들어 앞으로 AX 프로젝트에서는 다음 형태가 됩니다.

```text
React
  ↓
FastAPI
  ↓
PostgreSQL
```

또는 AI 서비스를 추가하면:

```text
React
  ↓
FastAPI
  ├── PostgreSQL
  ├── LangChain
  ├── RAG
  └── LLM API
```

### 비전공자 첫 수업이라면

FastAPI를 처음 가르칠 때는 처음부터 DB나 React까지 연결하기보다,

**1단계:** `GET` → **2단계:** Path Parameter → **3단계:** Query Parameter → **4단계:** `POST + JSON` → **5단계:** React 연동 → **6단계:** PostgreSQL 연결

순서가 이해하기 가장 좋습니다.

특히 처음에는 **`main.py` 파일 하나 + `/docs`에서 API 테스트**만으로 실습시키면 학생들이 프론트엔드와 백엔드의 차이를 비교적 빠르게 이해할 수 있습니다.
