from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Response
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import TodoCreate, TodoPatch, TodoOut, TodoPage
from .todo_service import TodoService
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
