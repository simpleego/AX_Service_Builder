"""
📌 3~4일차 실습 — 인증 비즈니스 로직
서비스 계층은 '무엇을 할 것인가'를 담당합니다. DB 세부사항은 repository에 맡기세요.
"""
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core import security
from app.core.config import settings
from app.repositories import user_repository, session_repository


def signup(db: Session, email: str, password: str):
    """
    TODO (3일차):
    1. 이미 가입된 이메일인지 확인 (user_repository.get_by_email)
       -> 있으면 HTTPException(400, "이미 가입된 이메일입니다.")
    2. 비밀번호를 해싱 (security.hash_password)
    3. user_repository.create로 사용자 생성 후 반환
    """
    raise NotImplementedError


def login(db: Session, email: str, password: str):
    """
    TODO (3일차):
    1. 이메일로 사용자 조회
    2. 사용자가 없거나, 비밀번호가 틀리면 -> HTTPException(401, "이메일 또는 비밀번호가 올바르지 않습니다.")
       💡 "이메일이 없다"와 "비밀번호가 틀렸다"를 구분해서 알려주지 마세요 (보안 관례)
    3. 통과하면 issue_tokens(db, user.id) 호출해서 반환
    """
    raise NotImplementedError


def issue_tokens(db: Session, user_id: int) -> dict:
    """
    TODO (4일차): 로그인/소셜로그인 공통으로 쓰이는 토큰 발급 함수
    1. security.create_access_token으로 access_token 생성
    2. security.generate_refresh_token으로 원본 refresh token 생성
    3. security.hash_refresh_token으로 해시 생성
    4. 만료시각 계산 (settings.REFRESH_TOKEN_EXPIRE_DAYS 일 후)
    5. session_repository.create로 해시를 DB에 저장 (원본은 저장하지 않음!)
    6. {"access_token":..., "refresh_token": 원본, "token_type": "bearer"} 반환
    """
    raise NotImplementedError


def refresh_access_token(db: Session, raw_refresh_token: str) -> dict:
    """
    TODO (4일차):
    1. raw_refresh_token을 해시
    2. session_repository.get_valid_by_hash로 유효한 세션 조회
    3. 없으면 -> HTTPException(401, "Refresh Token이 유효하지 않거나 만료되었습니다. 다시 로그인해주세요.")
    4. 있으면 session.user_id로 새 access_token 발급해서 반환
    """
    raise NotImplementedError


def logout(db: Session, raw_refresh_token: str) -> None:
    """
    TODO (4일차):
    1. 토큰 해시
    2. 유효한 세션을 찾아 session_repository.revoke로 폐기
       (세션이 없으면 그냥 조용히 넘어가도 됩니다 — 이미 로그아웃된 상태로 취급)
    """
    raise NotImplementedError
