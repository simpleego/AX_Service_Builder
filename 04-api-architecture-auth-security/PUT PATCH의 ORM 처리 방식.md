# PUT, PATCH의 ORM 처리 방식

네. FastAPI에서 SQLAlchemy 같은 ORM을 사용하면 PUT과 PATCH 요청을 모두 처리할 수 있습니다. 하지만 ORM이 HTTP 요청 방식에 따라 수정 범위를 자동으로 판단해 주는 것은 아닙니다.

즉, 개발자가 PUT과 PATCH의 처리 규칙을 정의해야 합니다.

다만 수정할 데이터만 결정하면 실제 SQL `UPDATE` 문 생성과 실행은 ORM이 자동으로 수행할 수 있으므로 개발자가 SQL을 직접 작성할 필요는 없습니다.

## 1. ORM에서 PUT과 PATCH를 처리하는 원리

### FastAPI + Pydantic + SQLAlchemy 처리 흐름

클라이언트

PUT /users/1 또는 PATCH /users/1

FastAPI Router + Pydantic DTO

요청 JSON을 Python 객체로 변환하고 검증

PUT

전체 필드 처리

PATCH

전달된 필드만 처리

SQLAlchemy ORM

Entity 속성 변경 감지 → SQL UPDATE 생성

Database

변경된 데이터 저장

### 개발자와 ORM의 역할

| 작업                | 담당                          |
| ----------------- | --------------------------- |
| PUT/PATCH 요청 구분   | FastAPI 라우터                 |
| JSON 데이터 검증       | Pydantic                    |
| 전체 교체 또는 부분 수정 정책 | 개발자                         |
| 수정할 ORM 객체의 속성 설정 | 개발자 코드                      |
| 변경된 속성 추적         | SQLAlchemy                  |
| SQL UPDATE 생성     | SQLAlchemy                  |
| SQL 실행 및 트랜잭션 반영  | SQLAlchemy + 개발자의 commit 제어 |

이것이 ORM을 사용할 때의 핵심적인 책임 분담입니다.

## 2. SQLAlchemy ORM으로 PUT과 PATCH 구현하기

SQLAlchemy 2.0 기준으로 두 가지 방식을 실제 코드로 비교하겠습니다.

### ① SQLAlchemy Entity 정의

먼저 DB 테이블에 대응하는 ORM 모델을 만듭니다.

```
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_columnclass Base(DeclarativeBase):    passclass User(Base):    __tablename__ = "users"    id: Mapped[int] = mapped_column(primary_key=True)    name: Mapped[str]    email: Mapped[str]    age: Mapped[int]
```

### ② Pydantic DTO 정의

PUT과 PATCH의 요청 DTO를 구분합니다.

```
from pydantic import BaseModel# PUT: 모든 필드 필수class UserReplace(BaseModel):    name: str    email: str    age: int# PATCH: 일부 필드만 전송 가능class UserPatch(BaseModel):    name: str | None = None    email: str | None = None    age: int | None = None
```

### ③ PUT: 전체 데이터 교체

```
@app.put("/users/{user_id}")def put_user(    user_id: int,    data: UserReplace,    db: Session = Depends(get_db)):    user = db.get(User, user_id)    if user is None:        raise HTTPException(404, "사용자가 없습니다.")    # 모든 수정 가능 필드에 값을 대입    user.name = data.name    user.email = data.email    user.age = data.age    db.commit()    db.refresh(user)    return {"message": "전체 수정 완료"}
```

위에서 개발자가 직접 수정하는 부분은 다음 세 줄입니다.

```
user.name = data.nameuser.email = data.emailuser.age = data.age
```

그 이후 SQLAlchemy가 변경 사항을 추적하고, `commit()` 과정에서 필요한 SQL을 생성합니다.

### ④ PATCH: 일부 데이터 수정

```
@app.patch("/users/{user_id}")def patch_user(    user_id: int,    data: UserPatch,    db: Session = Depends(get_db)):    user = db.get(User, user_id)    if user is None:        raise HTTPException(404, "사용자가 없습니다.")    changes = data.model_dump(exclude_unset=True)    for field, value in changes.items():        setattr(user, field, value)    db.commit()    db.refresh(user)    return {"message": "부분 수정 완료"}
```

여기서 가장 중요한 코드는 두 부분입니다.

첫 번째: 실제로 요청받은 필드만 추출

```
changes = data.model_dump(exclude_unset=True)
```

요청:

```
{
  "email": "new@example.com"
}
```

`changes` 결과:

```
{"email": "new@example.com"}
```

두 번째: ORM 객체의 속성을 동적으로 변경

```
for field, value in changes.items():    setattr(user, field, value)
```

`setattr()`은 Python 객체의 속성값을 변경하는 내장 함수입니다.

따라서 위 코드는 다음 코드와 동일한 효과가 있습니다.

```
user.email = "new@example.com"
```

SQLAlchemy는 이 속성 변경을 추적하고, 필요할 때 `UPDATE` SQL을 생성합니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.sqlalchemy.org\&sz=32)

SQLAlchemy 2.0 Documentation+1



이 예제는 `UserPatch` DTO에서 수정 가능한 컬럼을 제한하고 있습니다. 실제 서비스에서는 명시적인 `null` 처리, 권한 검증, DB 제약 조건도 함께 고려해야 합니다.

## 3. ORM이 SQL을 어떻게 생성하는가?

예를 들어 다음의 PATCH 요청이 들어왔다고 가정하겠습니다.

```
{
  "email": "new@example.com"
}
```

ORM 내부 처리 과정

1\. 데이터 조회

`user = db.get(User, 1)`

2\. 속성 변경

`user.email = "new@example.com"`

3\. SQLAlchemy 변경 감지

Unit of Work / Dirty Checking

4\. commit 시 SQL 생성 및 실행

```
UPDATE users
SET email = 'new@example.com'
WHERE id = 1;
```

DB 트랜잭션 반영 완료

실제로는 SQLAlchemy가 바인딩 파라미터를 사용하며, 변경된 속성에 따라 SQL이 달라집니다. 속성에 같은 값을 다시 대입했다면 실질적인 변경이 없다고 판단하여 `UPDATE`를 생략할 수도 있습니다.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://docs.sqlalchemy.org\&sz=32)

SQLAlchemy 2.0 Documentation+1



## 4. 그러면 PUT과 PATCH의 처리 범위를 개발자가 수동으로 제어해야 하나?

네. 하지만 매번 SQL을 직접 작성하는 수준의 수동 제어는 아닙니다.

개발자가 결정하는 것은 다음과 같습니다.

| 항목       | 개발자가 결정하는 내용                |
| -------- | --------------------------- |
| 요청 DTO   | PUT은 전체 필드 필수, PATCH는 선택 필드 |
| 수정 정책    | 전체 교체 또는 일부 변경              |
| 필드 허용 범위 | ID, 권한, 생성일 등 수정 금지         |
| 검증       | 필수값, 이메일 형식, 범위 등           |
| DB 처리    | commit, rollback, 예외 처리     |
| 동시성      | 필요한 경우 버전 검사나 잠금 적용         |

반면 SQLAlchemy의 변경 감지, SQL 생성, 파라미터 바인딩은 ORM이 담당합니다.

## 5. Spring JPA와 비교하면?

Spring JPA의 영속성 컨텍스트와 상당히 유사합니다.

```
@Transactional
public void updateUser(Long id, UserDto dto) {
    User user = repository.findById(id)
        .orElseThrow();

    user.setEmail(dto.email());

    // 트랜잭션 커밋 시 변경 감지 후 UPDATE 실행
}
```

SQLAlchemy에서도 비슷한 흐름으로 구현합니다.

```
user = db.get(User, id)user.email = data.emaildb.commit()
```

Spring JPA는 `@Transactional`이 관리하는 트랜잭션 종료 시점에 변경 사항이 반영될 수 있고, SQLAlchemy는 `Session`의 flush와 commit을 통해 변경 사항을 반영합니다.

두 기술 모두 Dirty Checking(변경 감지) 개념을 이용하지만, 트랜잭션 관리 방법에는 차이가 있습니다.

## 6. 실무적으로 권장하는 구현 방식

비전공자 교육이라면 PUT과 PATCH를 다음처럼 정리하면 명확합니다.

```
# PUT: 전체 필드 대입for field, value in data.model_dump().items():    setattr(user, field, value)# PATCH: 요청에 포함된 필드만 대입for field, value in data.model_dump(exclude_unset=True).items():    setattr(user, field, value)# 공통 처리db.commit()
```

이 코드는 요청 DTO가 허용된 수정 필드만 정의하고 있다는 전제에서 사용해야 합니다.

핵심은 `model_dump()`와 `model_dump(exclude_unset=True)`의 차이입니다.

- `model_dump()`는 모델의 전체 필드를 반환합니다.
- `model_dump(exclude_unset=True)`는 요청에서 명시적으로 전달한 필드만 반환합니다.

단, `exclude_unset=True`에서도 클라이언트가 명시적으로 보낸 `null`은 포함됩니다.

최종 결론: FastAPI + SQLAlchemy에서는 개발자가 PUT/PATCH의 수정 정책과 ORM 객체에 대입할 필드를 결정하고, SQLAlchemy가 변경 감지와 SQL 생성을 담당합니다. Spring JPA에서 DTO의 값을 Entity에 반영하고 Dirty Checking으로 저장하는 방식과 본질적으로 유사합니다.
