"""📌 1일차(REST 설계) + 6일차(소유권 기반 접근 제어·태그 필터링) 실습"""
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.todo import TodoCreate, TodoUpdate, TodoOut
from app.services import todo_service
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/todos", tags=["할일"])


@router.post("", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(
    payload: TodoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """TODO: todo_service.create_todo를 current_user.id로 호출하세요."""
    raise NotImplementedError


@router.get("", response_model=list[TodoOut])
def list_todos(
    tag: Optional[str] = Query(None, description="태그 이름으로 필터"),
    status_filter: Optional[str] = Query(None, alias="status", description="todo|in_progress|done"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """TODO: todo_service.list_my_todos 호출."""
    raise NotImplementedError


@router.get("/{todo_id}", response_model=TodoOut)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """TODO: todo_service.get_owned_todo 호출. (여기서 403이 자동 처리됨을 확인하세요)"""
    raise NotImplementedError


@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    TODO:
    1. payload.model_dump(exclude={"tag_names"}, exclude_unset=True)로 data 딕셔너리 생성
    2. todo_service.update_todo(db, current_user.id, todo_id, data, payload.tag_names) 호출
    """
    raise NotImplementedError


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """TODO: todo_service.delete_todo 호출."""
    raise NotImplementedError
