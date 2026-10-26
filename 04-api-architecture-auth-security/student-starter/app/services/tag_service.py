"""📌 6일차 실습"""
from sqlalchemy.orm import Session

from app.repositories import tag_repository


def list_tags(db: Session):
    """TODO: tag_repository.list_all 호출."""
    raise NotImplementedError


def create_tag(db: Session, name: str):
    """TODO: tag_repository.get_or_create 호출."""
    raise NotImplementedError
