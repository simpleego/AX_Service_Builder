"""📌 6일차 실습 — 이 파일의 핵심은 '소유권 검증(인가)'입니다."""
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories import todo_repository, tag_repository
from app.models.todo import Todo


def create_todo(db: Session, user_id: int, title: str, content, due_date, tag_names: list[str]):
    """
    TODO:
    1. todo_repository.create로 Todo 생성
    2. _apply_tags로 태그 연결
    3. todo_repository.get_by_id로 태그까지 포함해서 다시 조회 후 반환
    """
    raise NotImplementedError


def list_my_todos(db: Session, user_id: int, tag_name: str | None, status_filter: str | None):
    """TODO: todo_repository.list_by_user 호출."""
    raise NotImplementedError


def get_owned_todo(db: Session, user_id: int, todo_id: int) -> Todo:
    """
    TODO — 이 함수가 6일차의 핵심입니다. 인증(누구인지) 다음 단계인 인가(권한이 있는지)를 확인합니다.
    1. todo_repository.get_by_id로 조회
    2. 없으면 -> HTTPException(404, "할일을 찾을 수 없습니다.")
    3. todo.user_id가 요청자(user_id)와 다르면
       -> HTTPException(403, "본인의 할일만 접근할 수 있습니다.")
       💡 왜 401이 아니라 403인지 강의안 6일차 표를 참고하세요.
    4. 통과하면 todo 반환
    """
    raise NotImplementedError


def update_todo(db: Session, user_id: int, todo_id: int, data: dict, tag_names: list[str] | None):
    """
    TODO:
    1. get_owned_todo로 소유권 확인된 todo를 가져온다 (여기서 403이 자동으로 처리됨)
    2. data 딕셔너리의 값들을 setattr로 todo에 반영 (None이 아닌 값만)
    3. tag_names가 주어졌으면 _apply_tags(..., replace=True)
    4. todo_repository.save로 저장 후 반환
    """
    raise NotImplementedError


def delete_todo(db: Session, user_id: int, todo_id: int) -> None:
    """TODO: get_owned_todo로 확인 후 todo_repository.delete 호출."""
    raise NotImplementedError


def _apply_tags(db: Session, todo: Todo, tag_names: list[str], replace: bool = False):
    """
    TODO:
    - replace=True면 todo.tags를 빈 리스트로 초기화
    - tag_names를 순회하며 tag_repository.get_or_create로 태그를 가져와 todo.tags에 추가
      (이미 들어있으면 중복 추가하지 않기)
    - 마지막에 db.commit()
    """
    raise NotImplementedError
