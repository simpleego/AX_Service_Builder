# ORM - FastAPI

---- 

<img width="1055" height="1491" alt="image" src="https://github.com/user-attachments/assets/2c373644-2be3-414d-aee2-59df81d59d51" />

---

FastAPI Todo 앱에서 ORM(주로 SQLAlchemy 사용)을 통해 새로운 '할 일(Todo)'을 등록하는 과정은 클라이언트의 데이터 요청부터 DB 저장 및 검증까지의 데이터 변환 계층을 거쳐 처리됩니다.

1. 흐름 시각화 (시퀀스 다이어그램)

데이터가 클라이언트로부터 들어와 DB에 영속화(Persistence)되고 응답으로 반환되기까지의 전체 흐름입니다.
[ Client ]          [ Pydantic Schema ]         [ FastAPI Router ]          [ ORM (SQLAlchemy) ]          [ Database ]

    |                        |                          |                           |                          |
    |--- JSON 데이터 전달 --->|                          |                           |                          |
    |    (title, description)|--- 유효성 검증 (Validation) |                           |                          |
    |                        |=========================>|                           |                          |
    |                        |    (TodoCreate 객체 변환)  |                           |                          |
    |                        |                          |--- DB 세션(db) 주입 받음    |                          |
    |                        |                          |--- ORM 모델 객체 생성 ---->|                          |
    |                        |                          |    (Todo(**todo.dict()))  |                          |
    |                        |                          |                           |--- db.add(new_todo) ---->| (Staging)
    |                        |                          |                           |--- db.commit() --------->| (영구 저장)
    |                        |                          |                           |<-- db.refresh(new_todo)-| (생성된 ID 반영)
    |                        |<-- Response 모델로 변환 ----|                           |                          |
    |<-- JSON 데이터 응답 -----|--------------------------|                           |                          |

2. 단계별 상세 과정 및 핵심 코드

할 일 등록 과정의 핵심은 검증용 객체인 Pydantic Schema를 데이터베이스 테이블과 매핑되는 ORM Model 객체로 변환하여 DB 세션에 전달하는 것입니다.

① 요청 데이터 수신 및 검증 (Pydantic Schema)

클라이언트가 보낸 JSON 데이터가 API 스펙에 맞는지 검증하고 파이썬 객체로 변환합니다.
python
from pydantic import BaseModel

class TodoCreate(BaseModel):
    title: str
    description: str | None = None
코드를 사용할 때는 주의가 필요합니다.

② ORM 테이블 모델 정의 (SQLAlchemy Model)

데이터베이스의 todos 테이블과 매핑될 파이썬 클래스입니다.
python
from sqlalchemy import Column, Integer, String, Boolean
from database import Base  # 선언적 베이스 클래스

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)
코드를 사용할 때는 주의가 필요합니다.

③ 라우터를 통한 등록 처리 (FastAPI Router)

Depends를 통해 DB 세션을 주입받고, 검증된 TodoCreate 데이터를 Todo ORM 객체로 만들어 저장합니다.
python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db  # DB 세션을 생성하는 제너레이터 함수
import models, schemas

router = APIRouter()

@router.post("/todos/", response_model=schemas.TodoResponse)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    # 1. Pydantic 스키마 데이터를 ORM 모델 객체로 변환
    db_todo = models.Todo(title=todo.title, description=todo.description)
    
    # 2. DB 세션 트랜잭션에 객체 추가 (Staging 상태)
    db.add(db_todo)
    
    # 3. 데이터베이스에 트랜잭션 커밋 (실제 DB에 반영 및 저장)
    db.commit()
    
    # 4. DB에서 생성된 자동 증가 ID(PK) 등을 불러오기 위해 객체 새로고침
    db.refresh(db_todo)
    
    # 5. response_model 스펙에 맞게 자동으로 JSON 변환되어 클라이언트에 응답
    return db_todo
코드를 사용할 때는 주의가 필요합니다.

3. 핵심 메커니즘 요약

• db.add(): 데이터베이스에 즉시 쓰는 것이 아닌, SQLAlchemy 세션이 관리하는 '영속성 컨텍스트'에 객체를 추가합니다.
• db.commit(): 이 시점에 실제 데이터베이스에 INSERT INTO todos ... SQL 쿼리가 실행되어 트랜잭션이 완료됩니다.
• db.refresh(): 데이터베이스가 자동으로 생성한 id 값이나 기본값(completed=False)을 파이썬 객체에 다시 동기화하여 최신 상태로 만들어 줍니다. [1] (https://www.reddit.com/r/learnpython/comments/16rodlt/i_followed_this_tutorial_to_make_a_todo_list_app/?tl=ko)
이 설계 구조를 사용하면 개발자가 복잡한 SQL문을 직접 작성하지 않고도 안전하게 유효성 검사를 거친 데이터를 데이터베이스에 등록할 수 있게 됩니다.
이 과정 중에서 비동기 처리(AsyncSession) 방식으로 변경하는 방법이나, 데이터베이스 연결 설정(get_db) 코드가 추가로 필요하신가요?

