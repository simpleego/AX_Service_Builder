from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Todo
class TodoRepository:
    def __init__(self, db: Session):
        self.db = db
    def list(self, owner: int, page: int, limit: int, completed: bool | None):
        query = select(Todo).where(Todo.owner_id == owner)
        if completed is not None:
            query = query.where(Todo.completed == completed)
        # SQLAlchemy가 입력값을 바인딩하므로 문자열 결합 SQL을 작성하지 않는다.
        return self.db.scalars(query.order_by(Todo.id.desc()).offset((page-1)*limit).limit(limit)).all()
    def find(self, owner: int, todo_id: int):
        # 상세/수정/삭제 모두 소유권을 SQL 조건에 넣어 IDOR를 방지한다.
        return self.db.scalar(select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner))
    def add(self, owner: int, values: dict):
        todo = Todo(owner_id=owner, **values)
        self.db.add(todo)
        return todo


from fastapi import HTTPException
from .schemas import TodoCreate, TodoPatch
class TodoService:
    def __init__(self, db):
        self.db, self.repo = db, TodoRepository(db)
    def list(self, owner, page, limit, completed):
        return {'data': self.repo.list(owner, page, limit, completed), 'page': page, 'limit': limit}
    def get(self, owner, todo_id):
        todo = self.repo.find(owner, todo_id)
        if todo is None:
            # 타인의 Todo와 없는 Todo에 같은 404를 주어 존재 여부를 숨긴다.
            raise HTTPException(404, 'TODO_NOT_FOUND')
        return todo
    def create(self, owner, data: TodoCreate):
        todo = self.repo.add(owner, data.model_dump())
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def update(self, owner, todo_id, data: TodoPatch):
        todo = self.get(owner, todo_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def remove(self, owner, todo_id):
        self.db.delete(self.get(owner, todo_id))
        self.db.commit()


from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Response
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import TodoCreate, TodoPatch, TodoOut, TodoPage
from .identity import current_user
router = APIRouter(prefix='/api/todos', tags=['Todos'])
DB = Annotated[Session, Depends(get_db)]
Owner = Annotated[int, Depends(current_user)]
TodoId = Annotated[int, Path(gt=0, le=4294967295)]
# 컨트롤러는 HTTP 계약을, 서비스는 업무/트랜잭션을, 저장소는 데이터 조회를 담당한다.
@router.get('', response_model=TodoPage, summary='내 할 일 목록')
def list_todos(db: DB, owner: Owner, page: int = Query(1, ge=1, le=1000000),
               limit: int = Query(20, ge=1, le=100), completed: bool | None = None):
    return TodoService(db).list(owner, page, limit, completed)
@router.post('', response_model=TodoOut, status_code=201, summary='할 일 생성')
def create_todo(data: TodoCreate, response: Response, db: DB, owner: Owner):
    todo = TodoService(db).create(owner, data)
    response.headers['Location'] = f'/api/todos/{todo.id}'
    return todo
@router.get('/{todo_id}', response_model=TodoOut, summary='내 할 일 상세')
def get_todo(todo_id: TodoId, db: DB, owner: Owner):
    return TodoService(db).get(owner, todo_id)
@router.patch('/{todo_id}', response_model=TodoOut, summary='할 일 일부 수정')
def update_todo(todo_id: TodoId, data: TodoPatch, db: DB, owner: Owner):
    return TodoService(db).update(owner, todo_id, data)
@router.delete('/{todo_id}', status_code=204, summary='할 일 삭제')
def delete_todo(todo_id: TodoId, db: DB, owner: Owner):
    TodoService(db).remove(owner, todo_id)
    return Response(status_code=204)
