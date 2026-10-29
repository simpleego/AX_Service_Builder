# Postman 기본 사용법: 서버 요청 3가지 실습

Postman은 HTTP 요청을 서버에 보내고, 서버가 반환하는 응답을 확인하는 API 테스트 도구입니다.

프론트엔드(React)를 개발하기 전에도 Postman을 사용하면 FastAPI 백엔드가 정상적으로 동작하는지 확인할 수 있습니다.

이번에는 가장 기본적인 HTTP 요청 3가지를 실습하겠습니다.

| 요청 방식  | 목적     | 실습 내용      |
| ------ | ------ | ---------- |
| GET    | 데이터 조회 | 학생 목록 가져오기 |
| POST   | 데이터 생성 | 새로운 학생 등록  |
| DELETE | 데이터 삭제 | 특정 학생 삭제   |

## 1. 실습용 FastAPI 서버 준비

먼저 다음 코드를 `main.py`로 저장합니다.

```
from fastapi import FastAPI, HTTPExceptionfrom pydantic import BaseModelapp = FastAPI()# 임시 데이터베이스students = [    {"id": 1, "name": "홍길동", "score": 90},    {"id": 2, "name": "김철수", "score": 85}]class Student(BaseModel):    name: str    score: int# 1. 학생 목록 조회@app.get("/students")def get_students():    return students# 2. 학생 등록@app.post("/students", status_code=201)def create_student(student: Student):    new_id = max((s["id"] for s in students), default=0) + 1    new_student = {"id": new_id, **student.model_dump()}    students.append(new_student)    return new_student# 3. 학생 삭제@app.delete("/students/{student_id}")def delete_student(student_id: int):    for student in students:        if student["id"] == student_id:            students.remove(student)            return {"message": "삭제 완료"}    raise HTTPException(status_code=404, detail="학생 없음")
```

터미널에서 다음 명령어를 실행합니다.

```
pip install fastapi uvicorn
uvicorn main:app --reload
```

서버 주소는 `http://127.0.0.1:8000`입니다.

## 2. Postman에서 요청 보내기

[Mastering API Testing with Postman: A Complete Guide for Developers](https://images.openai.com/static-rsc-4/sGRFCAAanc0zJNhTO3S1brsIdtHdQy-lRmrijURgaVQ-RQYlHhAiLAmTLmwatjjIzInaEI4qmnHaKqRVY27QLVKfkxWwX19G6MuwstrQTZOgWW4LzUC_02RfRVd26s6dMfnc6Ed_Vu52gAuYCKbvPKyHy6q8etPX9d2HPEkFAt8?purpose=inline)

[Postman POST Requests](https://images.openai.com/static-rsc-4/UQI52XlIjZT9C_hCLz3M0DBvY6Kenutsqcqsj3asckYbvg3MgLsk5oxqBC1onodAfngDjOyJPaDMpDKbYBy5Rd53aK0Mgr_4jRXz3yQQM5d6llgy4cMucPHD_329HGX4TyY9Ua9tNM2tAQUxu_aiEsLs7Hm9JdGv-6GGOZc8iuk?purpose=inline)

[Mock 示例 | Postman 官方帮助文档中文版](https://images.openai.com/static-rsc-4/kK9Fnh6kxXyHfmQiucngciQ3mQGeUrmJJku9Cnz0zT7Jp_b2DnWnCfCf03PJiM8kxBVtNdd9m7TI55PAGwXM9hrqbko47o-P4rewHhMuu00-jvXeJFLnxvj8xS2JZ7O7-EteHKSnHcg0N542NneRDGd_c468FB4fd2DOjpsNlCY?purpose=inline)

4

Postman에서 공통적으로 사용하는 방법은 다음과 같습니다.

1. Postman을 실행하고 새 HTTP Request를 생성합니다.
2. HTTP 메서드(GET, POST, DELETE)를 선택합니다.
3. 서버 URL을 입력합니다.
4. 필요하면 `Body`, `Params`, `Headers`를 설정합니다.
5. Send 버튼을 눌러 요청을 전송합니다.
6. 하단의 응답 본문(Response Body)과 상태 코드(Status Code)를 확인합니다.

## 3. 실습 ① GET 요청 — 학생 목록 조회

GET

서버에 저장된 데이터를 가져오기

GET

[http://127.0.0.1:8000/students](http://127.0.0.1:8000/students?utm_source=chatgpt.com)

Send

Response · 200 OK

```
[
  {"id": 1, "name": "홍길동", "score": 90},
  {"id": 2, "name": "김철수", "score": 85}
]
```

실습 순서

1. 메서드를 `GET`으로 선택합니다.
2. URL에 `http://127.0.0.1:8000/students`를 입력합니다.
3. `Send`를 클릭합니다.
4. 응답 상태 `200 OK`와 학생 목록을 확인합니다.

GET 요청에서는 별도의 Body를 작성할 필요가 없습니다.

## 4. 실습 ② POST 요청 — 학생 등록

POST

서버에 새로운 데이터를 추가하기

POST

[http://127.0.0.1:8000/students](http://127.0.0.1:8000/students?utm_source=chatgpt.com)

Body → raw → JSON

```
{
  "name": "이영희",
  "score": 95
}
```

Response · 201 Created

```
{
  "id": 3,
  "name": "이영희",
  "score": 95
}
```

실습 순서

1. 메서드를 `POST`로 선택합니다.
2. URL을 `/students`로 지정합니다.
3. `Body` 탭 → `raw` 선택 → 형식을 `JSON`으로 지정합니다.
4. 위의 JSON 데이터를 입력한 후 `Send`를 클릭합니다.
5. 응답 `201 Created`를 확인합니다.

JSON 형식을 선택하면 일반적으로 `Content-Type: application/json` 헤더가 자동 설정됩니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://learning.postman.com\&sz=32)

Postman Docs



다시 GET 요청을 보내면 등록한 학생이 목록에 추가되어 있습니다.

## 5. 실습 ③ DELETE 요청 — 학생 삭제

DELETE

서버에 저장된 특정 데이터 삭제하기

DELETE

[http://127.0.0.1:8000/students/3](http://127.0.0.1:8000/students/3?utm_source=chatgpt.com)

Response · 200 OK

```
{
  "message": "삭제 완료"
}
```

실습 순서

1. 메서드를 `DELETE`로 선택합니다.
2. URL 끝에 삭제할 학생 ID인 `3`을 지정합니다.
3. `Send`를 클릭합니다.
4. 응답을 확인한 후 GET 요청을 다시 보내 학생이 삭제되었는지 확인합니다.

이 예시에서는 URL의 `3`이 FastAPI의 경로 매개변수 `student_id`로 전달됩니다.

## 6. 전체 요청과 응답 흐름

## 7. 세 가지 요청 비교

| 구분        | GET         | POST        | DELETE        |
| --------- | ----------- | ----------- | ------------- |
| 목적        | 조회          | 등록          | 삭제            |
| HTTP 메서드  | GET         | POST        | DELETE        |
| URL       | `/students` | `/students` | `/students/3` |
| Body      | 없음          | JSON 입력     | 없음            |
| 성공 코드     | 200         | 201         | 200           |
| 서버 데이터 변경 | 없음          | 추가          | 삭제            |

실습 시 주의사항: 이 예제는 DB 대신 파이썬 리스트에 데이터를 저장합니다. 따라서 서버를 재시작하면 등록하거나 삭제했던 내용이 초기 상태로 돌아갑니다.

처음 Postman을 학습할 때는 GET → POST → GET → DELETE → GET 순서로 실습하는 것이 좋습니다. 등록과 삭제 요청을 실행한 후 실제 데이터가 어떻게 변경되었는지 확인할 수 있기 때문입니다.

공식 참고 자료: [Postman 요청 생성 및 전송 가이드](https://learning.postman.com/docs/use/send-requests/create-requests/create-requests?utm_source=chatgpt.com)
