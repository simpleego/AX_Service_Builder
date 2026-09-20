# 학생 성적 계산 실습

Python 3.10 이상. main.py와 index.html을 같은 폴더에 둡니다.

## 실행 (Windows, 가상환경 활성화 불필요)

압축을 풀고 student_scores 폴더를 VS Code에서 열어 터미널에서 실행합니다.

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m uvicorn main:app --reload
```

브라우저: http://127.0.0.1:8000
API 실습: http://127.0.0.1:8000/docs

index.html을 더블클릭하거나 Live Server로 열지 않고 위 서버 주소로 접속합니다.
FastAPI가 화면과 API를 함께 제공하므로 별도의 CORS 설정이 필요 없습니다.
종료: 터미널에서 Ctrl+C.

## 동작

- 최초 1명, 학생 추가 버튼으로 최대 10명.
- 이름과 학과 필수(공백만 입력 불가), 점수는 0~100 정수.
- HTML required/min/max/step으로 기본 검증, JS trim으로 공백 검증.
- 학생별 객체를 students 배열에 push하고 JSON.stringify(students)로 전송.
- FastAPI가 list[Student]로 수신하며 인원·이름·학과·점수를 다시 검증.
- 학생별 세 과목 총점, 평균, 평균 기준 평점을 반환.
- 평균은 소수점 둘째 자리까지 표시하며 평점은 반올림 전 평균으로 판정.
- A: 90 이상, B: 80 이상 90 미만, C: 70 이상 80 미만,
  D: 60 이상 70 미만, F: 60 미만.
- 데이터베이스 저장 기능은 없으며 새로고침 시 입력이 초기화됩니다.

## 요청 JSON (POST /scores)

```json
[
  {"name":"김민수","department":"컴퓨터공학과","korean":90,"english":80,"math":100},
  {"name":"이영희","department":"경영학과","korean":70,"english":80,"math":75}
]
```

첫 학생: 총점 270, 평균 90.00, 평점 A.
둘째 학생: 총점 225, 평균 75.00, 평점 C.

## 핵심 개념

input.value는 문자열입니다. 점수는 Number(...)로 숫자로 변환합니다.
JS 객체 배열 → JSON.stringify → HTTP 요청 → Python 학생 목록.
Python 결과 목록 → JSON 응답 → response.json() → JS 객체 배열 → 표.

공식 참고: https://fastapi.tiangolo.com/tutorial/body-nested-models/
