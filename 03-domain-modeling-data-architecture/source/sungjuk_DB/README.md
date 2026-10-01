# 학생 성적 관리 · MariaDB CRUD

기존 `sungjuk02`의 FastAPI + HTML/CSS/JavaScript 구조를 확장한 수업용 예제입니다.

- 이름·학과·국어·영어·수학 점수를 MariaDB에 등록합니다.
- 전체 조회, 이름/학과 부분 검색, 개별 조회, 수정, 삭제를 지원합니다.
- **학생별 총점·평균·학점은 Python에서 계산**합니다. DB에는 입력값만 저장합니다.
- **과목별 인원·총점·평균·최소값·최대값은 SQL의 GROUP BY와 집계함수로 계산**합니다.
- 검색은 학생 목록에만 적용됩니다. 통계는 항상 **저장된 전체 학생** 기준입니다.
- 등록/수정/삭제 후 목록과 통계를 자동으로 다시 조회합니다.

## 파일 구성

| 파일 | 역할 |
|---|---|
| `main.py` | FastAPI CRUD, 학생별 Python 계산, 과목별 SQL 집계 |
| `database.py` | 환경변수 기반 MariaDB 연결, 커밋/롤백/연결 종료 |
| `index.html` | 등록·검색·수정·삭제·통계 UI |
| `schema.sql` | 데이터베이스·테이블 생성, 앱 계정 생성 예시 |
| `.env.example` | DB 접속 설정 예시 |
| `requirements.txt` | 실행 라이브러리 |
| `tests/test_app.py` | Python 계산·API 검증·SQL 집계 테스트 |
| `tests/test_mariadb.py` | 별도 테스트 DB에서 실행하는 실제 MariaDB 통합 테스트 |

## 1. MariaDB 준비

MariaDB를 실행하고 HeidiSQL에서 관리자 계정으로 접속합니다.
`schema.sql` 내용을 쿼리 탭에 붙여 넣고 실행하세요. 기존 자료를 삭제하는 구문은 없습니다.

다음으로 앱 전용 계정을 생성합니다. 비밀번호는 직접 정한 값으로 변경하세요.

```sql
CREATE USER IF NOT EXISTS 'sungjuk_app'@'127.0.0.1'
IDENTIFIED BY 'CHANGE_ME';
GRANT SELECT, INSERT, UPDATE, DELETE ON sungjuk_db.*
TO 'sungjuk_app'@'127.0.0.1';
```

이미 같은 계정이 있으면 `CREATE USER IF NOT EXISTS`는 비밀번호를 바꾸지 않습니다.
기존 비밀번호를 사용하거나 관리자 계정에서 `ALTER USER`로 변경하세요.
환경에 따라 MariaDB가 접속 호스트를 `localhost`로 판단하면 같은 권한의
`'sungjuk_app'@'localhost'` 계정을 만들어 사용하세요.

## 2. Windows / VS Code 실행

압축을 풀고 `sungjuk02` 폴더에서 터미널을 엽니다.
가상환경 활성화 없이 아래처럼 해당 Python을 직접 호출하면 됩니다.

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`를 열고 접속 계정과 비밀번호를 입력합니다.

```dotenv
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=sungjuk_app
DB_PASSWORD=CHANGE_ME
DB_NAME=sungjuk_db
```

비밀번호에 `#` 등 특수문자가 있으면 값을 따옴표로 감싸세요.
`.env`는 Git에 커밋하지 않습니다.

```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

- UI: http://127.0.0.1:8000/
- API 문서: http://127.0.0.1:8000/docs

**HTML을 Live Server의 5500 포트로 열지 말고 FastAPI의 8000 포트로 접속하세요.**
FastAPI가 HTML도 제공하므로 상대 경로 fetch가 올바른 API에 도달하고 별도 CORS 설정이 필요 없습니다.
서버는 `sungjuk02` 폴더에서 실행하세요.

Linux/macOS에서는 `python3 -m venv .venv`, `.venv/bin/python -m pip install -r requirements.txt`,
`cp .env.example .env`, `.venv/bin/python -m uvicorn main:app --reload`를 사용합니다.

## 3. 사용 순서와 확인 예시

1. 홍길동 / 컴퓨터공학 / 국어 90 / 영어 80 / 수학 70을 등록합니다.
   - 총점 240, 평균 80.00, 학점 B가 표시됩니다.
2. 김영희 / 경영학 / 국어 100 / 영어 90 / 수학 80을 등록합니다.
   - 국어: 인원 2, 총점 190, 평균 95.00, 최소 90, 최대 100
   - 영어: 인원 2, 총점 170, 평균 85.00, 최소 80, 최대 90
   - 수학: 인원 2, 총점 150, 평균 75.00, 최소 70, 최대 80
3. 이름 또는 학과로 조회합니다. 검색을 해도 통계는 두 학생 전체 기준입니다.
4. 홍길동의 `수정` 버튼 → 수학을 100으로 변경 → `수정 저장`을 누릅니다.
   - 총점 270, 평균 90.00, 학점 A, 수학 평균 90.00으로 갱신됩니다.
5. `삭제` 버튼을 누르면 확인창이 나오며 확인 후 해당 학생만 삭제됩니다.
6. 새로고침해도 DB에 저장된 성적이 유지됩니다.

같은 이름의 학생을 여러 명 등록할 수 있으며 고유 `id`로 수정·삭제 대상을 구분합니다.
0명일 때 과목별 인원/총점은 0, 평균/최소/최대는 `—`입니다.
빈 점수는 0점이며 평균 계산의 인원수에 포함됩니다.
기존 UI의 10명 입력 제한은 저장 목록에는 적용하지 않습니다. 한 번에 한 명씩 등록합니다.

## 4. API

| 메서드 | 경로 | 동작 |
|---|---|---|
| POST | `/students` | 한 명 등록, 201 |
| GET | `/students` | 전체 조회 |
| GET | `/students?q=홍` | 이름/학과 부분 검색 |
| GET | `/students/{id}` | 한 명 조회, 없으면 404 |
| PUT | `/students/{id}` | 이름·학과·점수 전체 수정 |
| DELETE | `/students/{id}` | 삭제, 성공 204 / 없으면 404 |
| GET | `/subjects` | 저장된 전체 학생의 과목별 SQL 통계 |
| POST | `/scores` | 기존 계산 전용 API, 학생 배열 1~10명, DB 저장 없음 |

등록/수정 JSON 예시:

```json
{"name":"홍길동","department":"컴퓨터공학","korean":90,"english":80,"math":70}
```

응답 예시:

```json
{"id":1,"name":"홍길동","department":"컴퓨터공학","korean":90,"english":80,"math":70,"total":240,"average":80.0,"grade":"B"}
```

이름과 학과는 필수이며 공백만 입력할 수 없습니다. 점수는 0~100 정수입니다.
점수의 누락/null/빈 문자열은 0으로 처리하지만 소수/음수/101/숫자 문자열/불리언은 거부합니다.
클라이언트가 총점·평균·학점을 보내도 입력으로 허용하지 않습니다.
기존 `POST /subjects/{subject}`의 화면 입력 기반 통계는 `GET /subjects`로 교체했습니다.

## 5. 계산 책임 분리

학생별 계산은 `calculate_result()`에서 처리합니다.

```python
total = student['korean'] + student['english'] + student['math']
average = total / 3
# 반올림 전 평균으로 A/B/C/D/F 판정 후 평균만 소수 둘째 자리로 반올림
```

DB에 계산값을 중복 저장하지 않아 점수 수정 후 총점이 오래된 값으로 남지 않습니다.

과목별 집계의 핵심 SQL은 다음과 같습니다.

```sql
SELECT subject,
       COUNT(*) AS student_count,
       SUM(score) AS total,
       ROUND(AVG(score), 2) AS average,
       MIN(score) AS minimum,
       MAX(score) AS maximum
FROM (
    SELECT 'korean' AS subject, korean AS score FROM students
    UNION ALL
    SELECT 'english', english FROM students
    UNION ALL
    SELECT 'math', math FROM students
) AS scores
GROUP BY subject;
```

가로로 저장한 국어·영어·수학 점수를 `UNION ALL`로 세로로 펼친 뒤 과목명으로 묶습니다.
`UNION`은 동일 점수 행을 제거할 수 있으므로 반드시 **UNION ALL**을 사용합니다.
실제 `main.py` SQL은 학생이 0명이어도 세 과목이 표시되도록 과목 목록과 `LEFT JOIN`합니다.
Python은 이 집계값을 재계산하지 않고 응답으로 전달합니다.

## 6. 검증과 범위

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
.\.venv\Scripts\python.exe -m pytest -q tests/test_app.py
```

단위/API 테스트는 격리된 SQLite 어댑터를 사용합니다. MariaDB 연결·권한·방언 확인을 대체하지 않습니다.
실제 MariaDB 통합 테스트는 `tests/test_mariadb.py`의 안내대로 **전용 테스트 DB**에서 실행하세요.

이 예제는 로컬 수업용이며 사용자 로그인/권한 관리가 없습니다. 서버 기본 바인딩인
127.0.0.1로 실습하세요. 대규모 목록의 페이지 나누기와 여러 사용자의 동시 편집 충돌 처리는
이 예제 범위에 포함하지 않았습니다.

### 이 전달본의 검증 결과

- Python/API 테스트: 18개 통과.
- DOM 이벤트 테스트: 등록, 검색, 수정, 삭제, 자동 통계 갱신, 빈 점수, 사용자 입력의 HTML 이스케이프 확인.
- JavaScript 문법 검사와 Git 공백 오류 검사 통과.
- MariaDB 실서버 연결 테스트: 서버 미설치로 미실행(통합 테스트 1개 건너뜀).
- 실제 브라우저 렌더링/레이아웃 검사: 브라우저 설치 제한으로 미실행.
- API/DOM 실행 검증의 DB는 격리된 SQLite 어댑터를 사용했습니다.
