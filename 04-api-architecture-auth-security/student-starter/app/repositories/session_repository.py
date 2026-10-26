"""📌 4일차 실습 — Refresh Token 저장소"""
from datetime import datetime, timezone
from sqlalchemy.orm import Session

from app.models.session import RefreshSession


def create(db: Session, user_id: int, token_hash: str, expires_at: datetime) -> RefreshSession:
    """TODO: RefreshSession 레코드를 생성·저장하세요."""
    raise NotImplementedError


def get_valid_by_hash(db: Session, token_hash: str) -> RefreshSession | None:
    """
    TODO: token_hash로 조회하되, 다음 조건을 모두 만족해야 '유효'합니다.
      1) revoked == False
      2) expires_at > 현재 시각
    힌트: datetime.now(timezone.utc)
    """
    raise NotImplementedError


def revoke(db: Session, session: RefreshSession) -> None:
    """TODO: session.revoked를 True로 바꾸고 commit하세요. (로그아웃 = 폐기)"""
    raise NotImplementedError
