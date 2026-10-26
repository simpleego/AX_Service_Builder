"""📌 2일차(기본 CRUD) + 6일차(태그 필터링) 실습"""
from sqlalchemy.orm import Session, joinedload

from app.models.todo import Todo
from app.models.tag import Tag


def create(db: Session, user_id: int, title: str, content: str | None, due_date) -> Todo:
    """TODO: Todo 생성·저장·반환."""
    raise NotImplementedError


def get_by_id(db: Session, todo_id: int) -> Todo | None:
    """
    TODO: id로 Todo 조회.
    힌트: .options(joinedload(Todo.tags)) 를 붙이면 태그를 한 번에 로딩해 N+1을 방지합니다.
    """
    raise NotImplementedError


def list_by_user(
    db: Session, user_id: int, tag_name: str | None = None, status: str | None = None
) -> list[Todo]:
    """
    TODO: 특정 사용자의 Todo 목록을 조건에 맞게 조회하세요.
      - user_id가 일치하는 것만
      - status가 주어지면 추가로 필터
      - tag_name이 주어지면 해당 태그를 가진 것만 (.join(Todo.tags).filter(Tag.name == tag_name))
    """
    raise NotImplementedError


def delete(db: Session, todo: Todo) -> None:
    """TODO: 삭제하고 commit."""
    raise NotImplementedError


def save(db: Session, todo: Todo) -> Todo:
    """TODO: 변경사항 commit + refresh 후 반환."""
    raise NotImplementedError
