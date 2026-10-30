# PUT, PATCH API SQL로 처리하는 방법

HTTP의 PUT과 PATCH는 모두 데이터를 수정하는 요청 방식이지만, SQL에서는 두 방식 모두 일반적으로 `UPDATE` 문을 사용합니다.

중요한 차이는 SQL 명령어 자체가 아니라, 어떤 컬럼을 어떻게 수정할 것인지 결정하는 서버의 처리 방식에 있습니다.

## 1. PUT과 PATCH를 SQL로 비교

예를 들어 다음과 같은 `users` 테이블이 있다고 가정하겠습니다.

```
CREATE TABLE users (
    id INT PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(100),
    age INT
);
```

현재 데이터는 다음과 같습니다.

| id | name | email            | age |
| -- | ---- | ---------------- | --- |
| 1  | 김철수  | old\@example.com | 20  |

### ① PUT: 리소스 전체 교체

클라이언트가 다음 요청을 전송합니다.

```
PUT /users/1
Content-Type: application/json
```

```
{
  "name": "이영희",
  "email": "new@example.com",
  "age": 25
}
```

서버는 전달받은 전체 데이터를 기준으로 사용자를 갱신합니다.

```
UPDATE users
SET
    name = '이영희',
    email = 'new@example.com',
    age = 25
WHERE id = 1;
```

실행 결과

| id | name | email            | age |
| -- | ---- | ---------------- | --- |
| 1  | 이영희  | new\@example.com | 25  |

모든 수정 가능 컬럼에 새로운 값을 지정했습니다.

다만 PUT이라고 해서 SQL에서 반드시 모든 컬럼을 `SET`에 포함해야 하는 것은 아닙니다. 핵심은 API가 요청 본문을 리소스의 새로운 전체 표현으로 해석한다는 것입니다.

### ② PATCH: 특정 컬럼만 수정

이번에는 이메일만 변경한다고 가정하겠습니다.

```
PATCH /users/1
Content-Type: application/json
```

```
{
  "email": "hello@example.com"
}
```

SQL에서는 다음과 같이 처리합니다.

```
UPDATE users
SET email = 'hello@example.com'
WHERE id = 1;
```

실행 결과

| id | name | email              | age |
| -- | ---- | ------------------ | --- |
| 1  | 이영희  | hello\@example.com | 25  |

이메일만 변경되고 나머지 데이터는 그대로 유지됩니다.

## 2. PUT 요청에서 일부 필드만 전송하면 어떻게 될까?

여기가 가장 중요합니다.

현재 데이터:

```
{
  "id": 1,
  "name": "김철수",
  "email": "old@example.com",
  "age": 20
}
```

클라이언트가 다음과 같이 요청한다고 가정하겠습니다.

```
PUT /users/1
```

```
{
  "name": "이영희"
}
```

PUT을 전체 교체 의미로 구현하고, 누락된 필드를 `NULL`로 취급한다면 다음과 같은 SQL이 실행될 수 있습니다.

```
UPDATE users
SET
    name = '이영희',
    email = NULL,
    age = NULL
WHERE id = 1;
```

결과:

| id | name | email | age  |
| -- | ---- | ----- | ---- |
| 1  | 이영희  | NULL  | NULL |

하지만 실제 동작은 API의 설계와 검증 규칙에 따라 달라집니다. 필수 필드가 누락되었다는 이유로 `400 Bad Request`나 `422 Unprocessable Content`를 반환할 수도 있습니다. 일부 서비스에서는 PUT을 부분 수정처럼 구현하기도 합니다.

따라서 교육에서는 PUT의 전체 교체 의미를 설명하고, 필수 필드 누락 시 요청을 거부하도록 구현하는 편이 명확합니다.

## 3. FastAPI에서는 실제로 어떻게 구현할까?

다음은 FastAPI와 SQL을 연결할 때 두 방식의 차이를 보여주는 예제입니다.

### PUT 구현

```
from fastapi import FastAPIfrom pydantic import BaseModelapp = FastAPI()class UserReplace(BaseModel):    name: str    email: str    age: int@app.put("/users/{user_id}")def replace_user(user_id: int, user: UserReplace):    sql = """        UPDATE users        SET name = :name,            email = :email,            age = :age        WHERE id = :id    """    params = {        "name": user.name,        "email": user.email,        "age": user.age,        "id": user_id    }    return {"sql": sql, "params": params}
```

위 예제는 SQL과 파라미터를 생성해 반환하는 교육용 코드이며, 실제 DB 실행은 포함하지 않았습니다.

`UserReplace`에서는 세 필드가 모두 필수이므로, 요청에서 하나라도 누락되면 FastAPI가 기본적으로 422 응답을 반환합니다.

### PATCH 구현

```
from fastapi import FastAPIfrom pydantic import BaseModelapp = FastAPI()class UserPatch(BaseModel):    name: str | None = None    email: str | None = None    age: int | None = None@app.patch("/users/{user_id}")def patch_user(user_id: int, user: UserPatch):    changes = user.model_dump(exclude_unset=True)    if not changes:        return {"message": "수정할 항목이 없습니다."}    set_clause = ", ".join(        f"{column} = :{column}" for column in changes    )    sql = f"""        UPDATE users        SET {set_clause}        WHERE id = :id    """    params = {**changes, "id": user_id}    return {"sql": sql, "params": params}
```

요청이 다음과 같다면

```
{
  "email": "new@example.com"
}
```

생성되는 SQL은 다음과 같습니다.

```
UPDATE users
SET email = :email
WHERE id = :id;
```

여기서 중요한 부분은 다음 코드입니다.

```
changes = user.model_dump(exclude_unset=True)
```

`exclude_unset=True`는 클라이언트가 전송하지 않은 필드를 제외합니다. 따라서 지정한 항목만 수정할 수 있습니다.

참고로 실제 운영 코드에서는 SQL 파라미터 바인딩과 함께, 수정 가능한 컬럼을 허용 목록으로 제한해야 합니다. 위 예제는 Pydantic 모델에 정의된 컬럼만 사용합니다. 또한 위 PATCH 모델은 명시적인 `null`도 허용하므로 DB의 `NOT NULL` 제약과 충돌하지 않도록 별도 검증이 필요합니다.

## 4. SQL 관점에서 핵심 차이 정리

| 구분         | PUT                      | PATCH           |
| ---------- | ------------------------ | --------------- |
| HTTP 의미    | 리소스 전체 교체                | 변경 사항 적용        |
| SQL 명령어    | `UPDATE`                 | `UPDATE`        |
| SQL SET 범위 | 일반적으로 수정 가능한 전체 컬럼       | 요청에서 지정한 컬럼     |
| 누락 필드      | API 정책에 따라 오류 또는 교체 시 반영 | 일반적으로 기존 값 유지   |
| 멱등성        | HTTP 표준상 멱등              | 구현 방식에 따라 다름    |
| 적합한 작업     | 전체 회원 정보 저장              | 이메일, 이름 등 일부 수정 |

## 5. 추가로 중요한 사항: PATCH도 멱등할 수 있다

다음 SQL은 몇 번 실행하더라도 최종 결과가 같습니다.

```
UPDATE users
SET age = 25
WHERE id = 1;
```

따라서 이런 PATCH는 멱등하게 구현할 수 있습니다.

반대로 다음 SQL은 실행할 때마다 나이가 증가합니다.

```
UPDATE users
SET age = age + 1
WHERE id = 1;
```

이런 증가 연산을 수행하는 PATCH는 멱등하지 않습니다.

결론적으로 PUT과 PATCH의 차이는 단순히 SQL의 `SET` 컬럼 개수로 구분하는 것이 아닙니다.

- PUT: 요청한 표현으로 리소스를 교체한다.
- PATCH: 요청에서 지정한 변경 사항을 적용한다.
- SQL: 두 경우 모두 `UPDATE`를 사용할 수 있으며, 실제 수정 범위는 백엔드 로직이 결정한다.

이러한 관점으로 설명하면 학생들이 HTTP 요청 방식과 데이터베이스 처리 방식을 명확하게 구분할 수 있습니다.
