"""
📌 3~6일차 공통 실습 — 현재 로그인한 사용자를 꺼내오는 의존성(DI)
라우터마다 인증 코드를 반복하지 않도록 여기 한 곳에 모읍니다.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core import security
from app.db.database import get_db
from app.models.user import User
from app.repositories import user_repository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login", auto_error=False)


def get_current_user(
    token: str | None = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    TODO:
    1. token이 없으면 -> 401 ("인증이 필요합니다.")
    2. security.decode_access_token(token)으로 user_id 추출
       -> None이면 401
    3. user_repository.get_by_id로 사용자 조회
       -> 없으면 401
    4. 사용자 객체 반환

    힌트: 401 응답에는 headers={"WWW-Authenticate": "Bearer"} 를 넣는 것이 관례입니다.
    """
    raise NotImplementedError
