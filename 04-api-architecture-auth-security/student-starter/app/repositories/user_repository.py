"""
📌 2일차 실습 — 리포지토리 계층
DB 접근만 담당합니다. 여기서 비즈니스 판단(예외 처리 등)을 하지 마세요 — 그건 service의 몫입니다.
"""
from sqlalchemy.orm import Session

from app.models.user import User


def get_by_email(db: Session, email: str) -> User | None:
    """TODO: email로 User 한 건을 조회해서 반환하세요. 없으면 None."""
    raise NotImplementedError


def get_by_id(db: Session, user_id: int) -> User | None:
    """TODO: id로 User 한 건을 조회해서 반환하세요."""
    raise NotImplementedError


def create(db: Session, email: str, password_hash: str | None) -> User:
    """
    TODO: User를 생성해 DB에 저장하고 반환하세요.
    순서: 객체 생성 -> db.add -> db.commit -> db.refresh -> return
    """
    raise NotImplementedError
