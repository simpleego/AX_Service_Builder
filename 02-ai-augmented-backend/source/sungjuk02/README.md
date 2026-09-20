# 학생 성적 계산 2차 버전

Python 3.10 이상. HTML/CSS/JS와 FastAPI로 구성합니다.

## 실행

압축을 풀고 student_scores_v2 폴더를 VS Code에서 연 후 터미널:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

브라우저에서 http://127.0.0.1:8000 접속. HTML을 더블클릭하거나 Live Server로 열지 않습니다.
이전 서버가 실행 중이라면 해당 터미널에서 Ctrl+C로 종료한 후 새 폴더에서 실행합니다.
API 실습: http://127.0.0.1:8000/docs

## 화면 및 계산 규칙

- 처음에는 1명. 학생 추가 버튼으로 최대 10명.
- 이름/학과/국어/영어/수학 오른쪽에 총점/평균/평점 readonly input을 배치.
- 학생별 계산 버튼: 화면의 모든 학생의 세 과목을 서버에서 계산하여 오른쪽에 표시.
- 표 하단에는 각 과목 열에 총점/평균/최고점/최저점 readonly input 및 과목별 버튼이 항상 표시됨.
- 국어 계산/영어 계산/수학 계산은 각각 독립적인 서버 요청이며 학생별 계산을 먼저 할 필요가 없음.
- 모든 계산 버튼은 화면의 세 과목 점수를 모두 검사. 범위 밖, 소수, 숫자가 아닌 입력은 차단.
- 빈 점수는 0점. 학생 평균의 분모는 3, 과목 평균의 분모는 현재 화면의 학생 행 수.
- 빈 행도 과목 통계 인원수에 포함하므로 최저점이 0점일 수 있음.
- 학생별 계산에는 이름/학과 필수. 과목별 계산에는 이름/학과가 없어도 됨.
- 평균은 소수점 둘째 자리까지 표시. 평점은 반올림 전 평균으로 판정.
- A >=90, B >=80, C >=70, D >=60, F <60.
- 입력 수정/학생 추가 시 이전 결과만 비우고 UI는 유지. 원하는 버튼으로 다시 서버 계산.
- 서버 요청 중에는 입력 및 버튼을 잠가 계산 중 데이터 변경 방지.
- 데이터는 저장하지 않으며 새로고침 시 초기화.

## 프론트 핵심

```javascript
student[key] = input.value === '' ? 0 : Number(input.value);
students.push(student);
const response = await fetch(url, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(students)
});
const result = await response.json();
```

실제 소스에서는 빈 값 변환 전에 input.reportValidity()로 잘못된 숫자를 검사합니다.
학생별/과목별 모두 현재 화면을 다시 읽어 객체 배열을 보내며, 계산은 서버에서 수행합니다.

## API

- POST /scores: 학생별 결과 배열 반환. 이름/학과 포함 list[Student].
- POST /subjects/korean: 국어 통계 반환.
- POST /subjects/english: 영어 통계 반환.
- POST /subjects/math: 수학 통계 반환.

요청 예시:
```json
[
  {"name":"김민수","department":"컴공","korean":90,"english":0,"math":100},
  {"name":"이영희","department":"경영","korean":0,"english":80,"math":70}
]
```

국어 통계 응답:
```json
{"total":90,"average":45.0,"maximum":90,"minimum":0}
```

서버도 인원(1~10)과 세 과목 점수(0~100 정수)를 검증합니다.
직접 API 호출 시 점수 누락/null/빈 문자열은 0점 처리합니다.

검증: 서버의 학생별/과목별 계산, 빈 값, 범위 오류, 인원 제한을 확인했습니다.
브라우저 자동 실행은 실행 환경에 Chromium이 없어 수행하지 못했습니다.
