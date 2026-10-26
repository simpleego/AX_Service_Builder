"""📌 1일차(REST 설계) + 3~4일차(인증) 실습"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.user import UserCreate, UserOut
from app.schemas.auth import (
    LoginRequest,
    TokenResponse,
    AccessTokenResponse,
    RefreshRequest,
    LogoutRequest,
)
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["인증"])


@router.post("/signup", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def signup(payload: UserCreate, db: Session = Depends(get_db)):
    """TODO: auth_service.signup을 호출하고 결과를 반환하세요."""
    raise NotImplementedError


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """TODO: auth_service.login을 호출하고 결과를 반환하세요."""
    raise NotImplementedError


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(payload: RefreshRequest, db: Session = Depends(get_db)):
    """TODO: auth_service.refresh_access_token을 호출하세요."""
    raise NotImplementedError


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(payload: LogoutRequest, db: Session = Depends(get_db)):
    """TODO: auth_service.logout을 호출하세요. (반환값 없음, 204)"""
    raise NotImplementedError
