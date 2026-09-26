# 프로그램 검증(Test)

> 이번에는 **Python/FastAPI를 학습한 학생들이 “테스트가 왜 필요한지 → 어떤 테스트가 있는지 → pytest로 어떻게 자동화하는지 → AI를 테스트에 어떻게 활용하는지”**까지 이어지도록 정리하겠습니다.

핵심은 다음입니다.

> **예외처리가 실행 중 발생한 문제에 대응하는 기술이라면, 테스트는 문제가 발생하기 전에 프로그램이 의도대로 동작하는지 검증하는 기술입니다.**

---

# 1. 테스트(Test)란 무엇인가?

프로그램을 작성했다고 해서 바로 정상 프로그램이라고 볼 수는 없습니다.

예를 들어 다음 함수가 있다고 하겠습니다.

```python
def add(a, b):
    return a + b
```

우리는 보통 다음 정도만 확인하고 넘어가기 쉽습니다.

```python
print(add(10, 20))
```

결과:

```text
30
```

그러면 이렇게 생각할 수 있습니다.

```text
30이 나왔다.
→ 프로그램 정상
```

하지만 실제로는 다양한 경우를 확인해야 합니다.

```text
add(10, 20)
add(0, 0)
add(-10, 20)
add(1.5, 2.5)
add("10", "20")
```

즉 테스트란:

> **입력값을 넣고 실제 결과가 우리가 예상한 결과와 같은지 자동 또는 수동으로 확인하는 과정**

입니다.

---

# 2. 예외처리와 테스트의 관계

두 개념을 구분하는 것이 중요합니다.

```text
예외처리
    ↓
실행 중 문제가 발생했을 때 대응

테스트
    ↓
문제가 존재하는지 미리 확인
```

예:

```python
def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None
```

예외처리를 했다고 해서 이 함수가 올바르게 만들어졌다는 뜻은 아닙니다.

그래서 테스트합니다.

```python
assert divide(10, 2) == 5
assert divide(10, 0) is None
```

---

# 3. 테스트의 가장 기본적인 방법

## 방법 1. 직접 실행

초보자들이 가장 먼저 사용하는 방식입니다.

```python
def add(a, b):
    return a + b


print(add(10, 20))
print(add(0, 0))
print(add(-10, 5))
```

단점은 사람이 결과를 직접 판단해야 합니다.

```text
30
0
-5
```

이 결과가 맞는지 사람이 확인해야 합니다.

---

# 4. assert를 이용한 테스트

Python에는 `assert`가 있습니다.

```python
def add(a, b):
    return a + b


assert add(10, 20) == 30
```

정상이면 아무 일도 발생하지 않습니다.

하지만:

```python
assert add(10, 20) == 40
```

이면:

```text
AssertionError
```

가 발생합니다.

즉:

```text
실제 결과 == 예상 결과
```

인지 확인하는 것입니다.

---

# 5. 테스트를 이해하는 가장 중요한 공식

학생들에게 다음 공식을 기억시키면 좋습니다.

```text
입력
 ↓
실행
 ↓
실제 결과
 ↓
예상 결과와 비교
 ↓
PASS / FAIL
```

이를 흔히 AAA 패턴이라고도 설명할 수 있습니다.

```text
Arrange
준비

Act
실행

Assert
검증
```

예:

```python
def add(a, b):
    return a + b


# Arrange
a = 10
b = 20

# Act
result = add(a, b)

# Assert
assert result == 30
```

---

# 6. 테스트 종류

실무에서는 테스트를 여러 단계로 구분합니다.

가장 기본적인 구분은 다음과 같습니다.

```text
Unit Test
    ↓
Integration Test
    ↓
System Test
    ↓
E2E Test
    ↓
Acceptance Test
```

---

# 7. Unit Test — 단위 테스트

가장 작은 단위를 테스트합니다.

보통:

```text
함수
메서드
클래스
```

정도를 테스트합니다.

예:

```python
def get_grade(score):

    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
```

테스트:

```python
assert get_grade(95) == "A"
assert get_grade(85) == "B"
assert get_grade(75) == "C"
assert get_grade(65) == "D"
assert get_grade(50) == "F"
```

이것이 전형적인 Unit Test입니다.

---

# 8. pytest 사용

Python 실무에서는 `pytest`를 많이 사용합니다.

설치:

```bash
pip install pytest
```

파일 구조:

```text
project/

├── calculator.py
└── test_calculator.py
```

`calculator.py`

```python
def add(a, b):
    return a + b


def divide(a, b):
    return a / b
```

`test_calculator.py`

```python
from calculator import add, divide


def test_add():
    assert add(10, 20) == 30


def test_divide():
    assert divide(10, 2) == 5
```

실행:

```bash
pytest
```

또는:

```bash
pytest -v
```

---

# 9. pytest의 기본 규칙

pytest는 보통 다음 이름을 자동으로 찾습니다.

파일:

```text
test_*.py
```

예:

```text
test_calc.py
test_student.py
test_order.py
```

함수:

```python
def test_xxx():
```

예:

```python
def test_add():
    pass


def test_order():
    pass
```

---

# 10. 예외 발생 테스트

예외처리 수업과 테스트를 연결하기 좋은 부분입니다.

다음 함수가 있다고 합시다.

```python
def divide(a, b):

    if b == 0:
        raise ValueError("0으로 나눌 수 없습니다.")

    return a / b
```

정상 테스트:

```python
def test_divide():

    assert divide(10, 2) == 5
```

예외 테스트:

```python
import pytest


def test_divide_zero():

    with pytest.raises(ValueError):

        divide(10, 0)
```

더 정확하게 확인할 수도 있습니다.

```python
def test_divide_zero():

    with pytest.raises(
        ValueError,
        match="0으로 나눌 수 없습니다."
    ):

        divide(10, 0)
```

---

# 11. 경계값 테스트

실무에서 매우 중요합니다.

예를 들어:

```python
def validate_score(score):

    if score < 0 or score > 100:
        raise ValueError()

    return True
```

많은 초보자가 다음만 테스트합니다.

```python
assert validate_score(50)
```

하지만 중요한 값은 경계입니다.

```text
-1
0
1

99
100
101
```

테스트:

```python
import pytest


def test_score_min():

    assert validate_score(0)


def test_score_max():

    assert validate_score(100)


def test_score_below():

    with pytest.raises(ValueError):
        validate_score(-1)


def test_score_above():

    with pytest.raises(ValueError):
        validate_score(101)
```

이것을 **Boundary Value Testing**이라고 합니다.

---

# 12. 동등분할 테스트

모든 값을 테스트할 수는 없습니다.

점수 범위:

```text
-∞ ~ -1
0 ~ 100
101 ~ ∞
```

처럼 그룹을 나눌 수 있습니다.

대표값을 선택합니다.

```text
-10
50
120
```

이를 동등분할이라고 합니다.

```text
Equivalence Partitioning
```

---

# 13. 정상·비정상 테스트

학생들에게 가장 쉽게 가르칠 수 있는 구분입니다.

예:

```python
def withdraw(balance, money):

    if money <= 0:
        raise ValueError("출금액 오류")

    if money > balance:
        raise ValueError("잔액 부족")

    return balance - money
```

정상 테스트:

```python
def test_withdraw():

    assert withdraw(50000, 10000) == 40000
```

비정상 테스트:

```python
def test_withdraw_over_balance():

    with pytest.raises(ValueError):

        withdraw(50000, 60000)
```

경계값:

```python
def test_withdraw_all():

    assert withdraw(50000, 50000) == 0
```

---

# 14. 테스트 케이스(Test Case)

테스트는 코드만 작성하는 것이 아니라 먼저 테스트 케이스를 설계하는 것이 좋습니다.

예:

| 번호 | 입력 | 예상결과 | 유형 |
|---:|---|---|---|
| 1 | 50000, 10000 | 40000 | 정상 |
| 2 | 50000, 50000 | 0 | 경계값 |
| 3 | 50000, 60000 | 잔액부족 | 예외 |
| 4 | 50000, 0 | 오류 | 예외 |
| 5 | 50000, -1000 | 오류 | 예외 |

이 표를 먼저 만들고 코드를 작성하는 습관이 좋습니다.

---

# 15. Integration Test — 통합 테스트

Unit Test는 함수 하나를 확인했다면, 통합 테스트는 여러 구성 요소가 연결되어 잘 동작하는지 확인합니다.

예:

```text
API
 ↓
Service
 ↓
Database
```

각각은 잘 작동하지만 연결 과정에서 문제가 발생할 수 있습니다.

예:

```text
Service → DB에 잘못된 SQL 전달

API → Service에 잘못된 자료형 전달

DB 결과 → 객체 변환 실패
```

따라서 연결 전체를 테스트합니다.

---

# 16. Mock 테스트

외부 시스템은 매번 실제로 호출하지 않는 경우가 많습니다.

예:

```python
def get_weather():

    result = call_weather_api()

    return result
```

테스트할 때 실제 날씨 API를 매번 호출하면 문제가 있습니다.

```text
인터넷 필요
API 비용 발생
응답시간 느림
API 서버 장애 영향
```

그래서 가짜 객체(Mock)를 사용합니다.

개념적으로:

```text
실제 Weather API

        ↓

Mock Weather API
```

로 바꾸는 것입니다.

---

# 17. Mock을 쉽게 이해하는 비유

식당 결제 프로그램을 테스트한다고 합시다.

실제 카드 결제 시스템을 매번 연결할 필요는 없습니다.

```text
결제요청
   ↓
가짜 카드회사

"결제 성공"
```

이라고 가짜 응답을 주면 됩니다.

이것이 Mock입니다.

---

# 18. FastAPI 테스트

FastAPI에는 `TestClient`를 이용한 테스트가 매우 편리합니다.

예:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():

    return {
        "message": "Hello"
    }
```

테스트:

```python
from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_hello():

    response = client.get("/hello")

    assert response.status_code == 200

    assert response.json() == {
        "message": "Hello"
    }
```

---

# 19. FastAPI 404 테스트

학생 조회 API:

```python
@app.get("/students/{student_id}")
def get_student(student_id: int):

    if student_id not in students:

        raise HTTPException(
            status_code=404,
            detail="학생을 찾을 수 없습니다."
        )

    return students[student_id]
```

테스트:

```python
def test_student_not_found():

    response = client.get(
        "/students/999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": "학생을 찾을 수 없습니다."
    }
```

이 테스트는 예외처리 수업과 연결하기 매우 좋습니다.

---

# 20. API 테스트에서 확인할 것

단순히 status code만 확인해서는 부족합니다.

보통 다음을 확인합니다.

```text
HTTP Status

Response Body

Response Header

데이터 구조

오류 메시지

DB 저장 결과
```

예:

```python
def test_create_student():

    response = client.post(
        "/students",
        json={
            "name": "홍길동",
            "score": 90
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "홍길동"
    assert data["score"] == 90
```

---

# 21. System Test

전체 시스템을 테스트합니다.

예:

```text
Frontend
 ↓
FastAPI
 ↓
Service
 ↓
PostgreSQL
```

전체가 실제 환경과 비슷하게 연결된 상태에서 확인합니다.

예:

```text
회원가입

로그인

상품조회

주문

결제

배송
```

---

# 22. E2E Test

End-to-End Test입니다.

사용자의 실제 행동 흐름을 테스트합니다.

예를 들어 쇼핑몰이라면:

```text
브라우저 실행
 ↓
로그인
 ↓
상품 검색
 ↓
장바구니
 ↓
결제
 ↓
주문 완료
```

실제 사용자가 하는 행동과 거의 동일합니다.

웹에서는 다음과 같은 도구를 활용할 수 있습니다.

```text
Playwright
Selenium
Cypress
```

Python 학습자라면 Playwright나 Selenium으로 연결하기 좋습니다.

---

# 23. 테스트 피라미드

실무 테스트 전략에서 중요한 개념입니다.

```text
               E2E
              /   \
             /     \
            /-------\
           Integration
          /-----------\
         /             \
        /---------------\
           Unit Test
```

보통:

```text
Unit Test
→ 많이

Integration Test
→ 적당히

E2E
→ 핵심 업무 위주
```

로 구성합니다.

그 이유는:

```text
Unit Test
빠름 / 저렴 / 원인 파악 쉬움

E2E
느림 / 유지보수 어려움 / 원인 파악 어려움
```

때문입니다.

---

# 24. 테스트의 중요한 분류

## 기능 관점

```text
Unit Test
Integration Test
System Test
E2E Test
Acceptance Test
```

## 코드 접근 관점

```text
White Box Test
Black Box Test
```

---

# 25. White Box Test

프로그램 내부 코드를 알고 테스트합니다.

예:

```python
def get_grade(score):

    if score >= 90:
        return "A"

    elif score >= 80:
        return "B"

    return "C"
```

개발자가 내부 분기 구조를 보고:

```text
90
89

80
79
```

같은 테스트를 설계합니다.

---

# 26. Black Box Test

내부 코드는 몰라도 됩니다.

다음 요구사항만 알고 있습니다.

```text
90 이상 A
80 이상 B
나머지 C
```

입력과 출력만 확인합니다.

```text
95 → A
85 → B
70 → C
```

---

# 27. 회귀 테스트 Regression Test

실무에서 매우 중요합니다.

프로그램을 수정했다고 합시다.

```text
기능 A 수정
```

그런데:

```text
기능 B가 고장남
```

이런 일이 매우 흔합니다.

그래서 기존 테스트를 다시 실행합니다.

```text
수정
 ↓
전체 테스트 실행
 ↓
기존 기능 이상 없음 확인
```

이것을 Regression Test라고 합니다.

---

# 28. 자동화 테스트가 필요한 이유

사람이 매번 테스트하면:

```text
로그인
상품 클릭
주문
결제
확인
```

을 계속 반복해야 합니다.

자동화하면:

```bash
pytest
```

한 번으로 많은 테스트를 실행할 수 있습니다.

CI/CD에서도:

```text
Git Push

 ↓

자동 Test

 ↓

PASS

 ↓

Build

 ↓

Deploy
```

구조를 만들 수 있습니다.

---

# 29. 이제 AI를 테스트에 어떻게 사용할까?

여기부터가 현재 매우 중요합니다.

AI가 테스트에서 할 수 있는 역할은 크게 두 가지입니다.

```text
① 기존 소프트웨어의 테스트를 AI가 도와준다.

② AI 시스템 자체를 테스트한다.
```

이 둘은 구분해야 합니다.

---

# 30. AI 활용 방법 ① 테스트 코드 생성

가장 쉽게 활용할 수 있는 방법입니다.

개발 코드:

```python
def get_grade(score):

    if score < 0 or score > 100:
        raise ValueError()

    if score >= 90:
        return "A"

    if score >= 80:
        return "B"

    return "C"
```

AI에게 다음처럼 요청할 수 있습니다.

```text
이 함수에 대해 pytest 테스트 코드를 작성해줘.

정상값
경계값
비정상값
예외발생

테스트를 모두 포함해줘.
```

AI가 다음 형태를 만들어 줄 수 있습니다.

```python
import pytest


def test_grade_a():
    assert get_grade(95) == "A"


def test_grade_90():
    assert get_grade(90) == "A"


def test_grade_b():
    assert get_grade(85) == "B"


def test_invalid_low():

    with pytest.raises(ValueError):
        get_grade(-1)


def test_invalid_high():

    with pytest.raises(ValueError):
        get_grade(101)
```

---

# 31. AI 활용 방법 ② 테스트 케이스 자동 생성

AI의 매우 좋은 활용 방법입니다.

요구사항:

```text
회원 나이는 14~100세

이름 필수

점수는 0~100

회원번호는 양의 정수
```

AI에게:

```text
위 요구사항을 기준으로

정상값
비정상값
경계값

테스트 케이스를 작성해줘.
```

라고 하면 다음과 같이 만들 수 있습니다.

| 항목 | 입력 | 예상결과 |
|---|---|---|
| 나이 | 14 | 정상 |
| 나이 | 13 | 오류 |
| 나이 | 100 | 정상 |
| 나이 | 101 | 오류 |
| 이름 | "" | 오류 |
| 점수 | 0 | 정상 |
| 점수 | 100 | 정상 |
| 점수 | 101 | 오류 |

즉 AI가 **테스트 설계 보조자** 역할을 합니다.

---

# 32. AI 활용 방법 ③ 빠진 테스트 찾기

실제로 매우 유용합니다.

개발자가 작성한 테스트:

```python
def test_score():

    assert get_grade(95) == "A"
    assert get_grade(85) == "B"
```

AI에게:

```text
이 테스트에서 누락된 테스트 케이스를 찾아줘.
```

라고 요청하면:

```text
90점 경계

89점 경계

80점 경계

79점 경계

0점

100점

-1

101

문자열 입력

None
```

등을 제안하게 할 수 있습니다.

이 방식은 AI를 **테스트 리뷰어**로 사용하는 것입니다.

---

# 33. AI 활용 방법 ④ 요구사항에서 테스트 자동 생성

예:

```text
상품 주문 시스템

1. 주문 수량은 1개 이상
2. 재고보다 많이 주문할 수 없음
3. 주문 완료 후 재고 감소
4. 재고가 없으면 주문 불가
```

AI에게:

```text
위 요구사항으로 테스트 시나리오를 작성해줘.
```

라고 할 수 있습니다.

AI가:

```text
TC01 정상 주문

TC02 주문수량 0

TC03 주문수량 -1

TC04 재고와 동일한 수량

TC05 재고보다 1개 많은 주문

TC06 재고 0
```

등을 만들어 줍니다.

이 방법은 상당히 실무적입니다.

---

# 34. AI 활용 방법 ⑤ 버그 가능성이 높은 부분 찾기

코드를 AI에게 제공하고:

```text
이 코드에서 버그가 발생할 가능성이 높은 부분을 찾아줘.

특히 다음을 확인해줘.

- None
- 빈 문자열
- 음수
- 0
- 최대값
- 범위 초과
- 타입 오류
- 예외처리 누락
```

등을 요청할 수 있습니다.

AI는 테스트 설계 전에 **위험 분석**을 수행할 수 있습니다.

---

# 35. AI 활용 방법 ⑥ 테스트 데이터 생성

예:

```text
학생 데이터 100개

정상 데이터 70%

경계값 10%

오류 데이터 20%
```

형태로 생성하게 할 수 있습니다.

예:

```python
[
    {
        "name": "홍길동",
        "score": 90
    },
    ...
]
```

다만 실제 개인정보를 AI에 그대로 제공하는 것은 주의해야 합니다.

---

# 36. AI 활용 방법 ⑦ API 테스트 생성

FastAPI 코드:

```python
@app.post("/students")
def create_student(student: StudentCreate):
    ...
```

를 AI에게 제공하고:

```text
FastAPI TestClient를 이용해

정상 등록
점수 -1
점수 0
점수 100
점수 101
이름 누락
score 누락
잘못된 타입

pytest 테스트를 만들어줘.
```

라고 요청할 수 있습니다.

이것은 현재 교육에서도 매우 좋은 실습입니다.

---

# 37. AI 활용 방법 ⑧ 실패한 테스트 분석

예:

```text
FAILED test_student.py::test_score

Expected: 90
Actual: 80
```

와 코드 일부를 AI에게 주고:

```text
테스트 실패 원인을 분석해줘.
```

라고 요청할 수 있습니다.

AI가:

```text
테스트가 잘못되었는지

실제 코드가 잘못되었는지

요구사항 해석이 잘못되었는지
```

를 비교하도록 사용할 수 있습니다.

---

# 38. 하지만 AI가 테스트의 정답은 아니다

매우 중요한 부분입니다.

AI가 작성한 테스트도 틀릴 수 있습니다.

예를 들어 요구사항이:

```text
90점 이상이면 A
```

인데 AI가 실수로:

```python
assert get_grade(90) == "B"
```

라고 만들 수도 있습니다.

따라서:

```text
요구사항

   ↓

사람이 테스트 기준 정의

   ↓

AI가 테스트 생성

   ↓

사람이 검토

   ↓

자동 테스트 실행
```

구조가 바람직합니다.

---

# 39. AI 활용 테스트의 가장 좋은 역할

AI에게 완전히 맡기기보다 다음 역할로 사용하는 것이 좋습니다.

```text
사람
→ 무엇이 정상인가 정의

AI
→ 가능한 테스트를 많이 생성

테스트 도구
→ 실제 실행

사람
→ 결과 판단
```

즉:

> **AI는 테스트 실행기가 아니라 테스트 설계와 분석을 보조하는 역할에서 특히 강력합니다.**

---

# 40. AI 프로그램 자체는 어떻게 테스트하는가?

이 부분은 일반 소프트웨어 테스트와 조금 다릅니다.

예를 들어 챗봇:

```text
사용자
↓
LLM
↓
답변
```

일반 프로그램은:

```text
2 + 3
→ 반드시 5
```

처럼 정답이 명확합니다.

하지만 LLM:

```text
Python이 뭐야?
```

에 대한 답은 하나가 아닙니다.

따라서 단순한:

```python
assert result == "..."
```

만으로 테스트하기 어렵습니다.

---

# 41. AI 시스템 테스트 평가 기준

예를 들어 RAG 챗봇이라면 다음을 평가합니다.

```text
정확성

관련성

근거성

검색 정확도

환각 여부

응답시간

비용
```

즉:

```text
AI Test

정답이 동일한가?
```

보다:

```text
좋은 답변인가?
```

를 평가하는 경우가 많습니다.

---

# 42. LLM-as-a-Judge

최근 AI 테스트에서 많이 사용하는 개념입니다.

하나의 AI가 생성한 답변을 다른 AI가 평가합니다.

예:

```text
질문

"FastAPI란 무엇인가?"
```

AI A:

```text
답변 생성
```

AI B:

```text
정확성
관련성
명확성
근거성
```

평가.

구조:

```text
User Question

      ↓

Application LLM

      ↓

Answer

      ↓

Judge LLM

      ↓

Score
```

---

# 43. 하지만 LLM-as-a-Judge 역시 완벽하지 않다

AI가 AI를 평가하더라도:

```text
평가 편향

모델 편향

채점 일관성

프롬프트 영향
```

이 있을 수 있습니다.

따라서 중요한 시스템에서는:

```text
자동 평가

+

사람 평가
```

를 함께 사용하는 것이 좋습니다.

---

# 44. RAG 시스템 테스트

현재 RAG를 배우고 있다면 이 부분이 특히 중요합니다.

RAG:

```text
질문

 ↓

검색

 ↓

관련 문서

 ↓

LLM

 ↓

답변
```

따라서 테스트도 나눠야 합니다.

```text
검색 Test

+

생성 Test
```

---

# 45. Retrieval Test

검색이 제대로 되었는지 확인합니다.

예:

```text
질문

"연차 휴가는 몇 일인가?"
```

정답 문서:

```text
인사규정 10조
```

테스트:

```text
검색 Top-3 안에
인사규정 10조가 있는가?
```

이런 방식으로 평가합니다.

대표적으로:

```text
Precision
Recall
Hit Rate
MRR
```

등을 사용할 수 있습니다.

---

# 46. Generation Test

검색된 문서를 바탕으로 생성한 답변을 평가합니다.

예:

```text
검색 문서와 답변이 일치하는가?

없는 내용을 만들지 않았는가?

질문에 실제로 답했는가?
```

평가 항목:

```text
Correctness

Relevance

Faithfulness

Groundedness
```

등을 사용할 수 있습니다.

---

# 47. AI 시대의 테스트 구조

정리하면 앞으로 테스트는 다음처럼 볼 수 있습니다.

```text
               Software Test

                     │

        ┌────────────┴────────────┐

        │                         │
전통 Software Test           AI System Test

        │                         │
Unit Test                 Retrieval Test
Integration Test          Generation Test
API Test                  Hallucination Test
E2E Test                  Safety Test
Regression Test           LLM Evaluation
```

---

# 48. 학생 수업에서 추천하는 학습 순서

비전공자라면 다음 순서가 적절합니다.

```text
1. print로 직접 테스트

        ↓

2. assert

        ↓

3. pytest

        ↓

4. 정상 / 비정상 테스트

        ↓

5. 경계값 테스트

        ↓

6. 예외 발생 테스트

        ↓

7. FastAPI TestClient

        ↓

8. Mock

        ↓

9. Integration Test

        ↓

10. AI로 테스트 케이스 생성

        ↓

11. AI로 테스트 코드 생성

        ↓

12. AI로 테스트 리뷰

        ↓

13. RAG / LLM 평가
```

---

# 49. 교육용으로 가장 중요한 하나의 예제

학생 성적 시스템을 기준으로 하면 전체 흐름을 연결하기 좋습니다.

개발 코드:

```python
def get_grade(score):

    if score < 0 or score > 100:
        raise ValueError(
            "점수는 0~100 사이여야 합니다."
        )

    if score >= 90:
        return "A"

    elif score >= 80:
        return "B"

    elif score >= 70:
        return "C"

    elif score >= 60:
        return "D"

    else:
        return "F"
```

기본 테스트:

```python
def test_grade():

    assert get_grade(95) == "A"
```

경계값 테스트:

```python
def test_grade_boundary():

    assert get_grade(90) == "A"
    assert get_grade(89) == "B"
```

예외 테스트:

```python
import pytest


def test_invalid_score():

    with pytest.raises(ValueError):

        get_grade(101)
```

그리고 AI에게:

```text
현재 get_grade 함수와 테스트 코드를 검토하고
누락된 경계값과 예외 테스트를 찾아줘.
```

라고 요청하게 합니다.

이렇게 하면 학생들이 **개발 → 예외처리 → 테스트 → AI 테스트 보조**를 하나의 흐름으로 이해할 수 있습니다.

---

# 50. 수업에서 강조할 최종 구조

학생들에게는 다음 그림을 보여주는 것이 가장 좋습니다.

```text
       개발자가 코드 작성

              ↓

          예외처리

     예상 가능한 오류 대응

              ↓

            Test

     프로그램 동작 검증

              ↓

          자동 Test

        pytest / API

              ↓

            AI

 테스트 케이스 생성
 테스트 코드 생성
 누락 테스트 탐색
 실패 원인 분석

              ↓

           CI/CD

      자동검증 → 배포
```

따라서 앞에서 배운 **예외처리의 다음 단계로 테스트를 배치하는 것이 매우 자연스럽습니다.**

> **예외처리는 “실패했을 때 어떻게 대응할 것인가”를 설계하고, 테스트는 “우리가 생각한 정상·실패 조건대로 실제로 작동하는가”를 검증합니다. AI는 그 과정에서 테스트 케이스 설계, 코드 생성, 누락 탐색, 실패 분석을 보조합니다.**

특히 현재 진행하시는 AX 과정이라면 다음 단계는 **`pytest → FastAPI TestClient → Mock → Integration Test → GitHub Actions 자동 테스트 → AI 기반 테스트 생성/리뷰 → LLM·RAG 평가`** 순서로 연결하는 것이 가장 교육 효과가 좋습니다.
