"""📌 6일차 실습 — 태그 저장소"""
from sqlalchemy.orm import Session

from app.models.tag import Tag


def get_by_name(db: Session, name: str) -> Tag | None:
    """TODO: name으로 Tag 조회."""
    raise NotImplementedError


def get_or_create(db: Session, name: str) -> Tag:
    """TODO: 이미 있으면 그걸 반환, 없으면 새로 만들어서 반환 (get_by_name 재사용)."""
    raise NotImplementedError


def list_all(db: Session) -> list[Tag]:
    """TODO: 전체 태그 목록 반환."""
    raise NotImplementedError
