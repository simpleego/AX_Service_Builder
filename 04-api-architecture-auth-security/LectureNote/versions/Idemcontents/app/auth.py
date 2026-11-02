from typing import Annotated
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .database import get_db
from .models import User, RefreshToken
from .security import now, digest, password_hash, password_matches, issue_tokens
router = APIRouter(prefix='/api/auth', tags=['Authentication'])
DB = Annotated[Session, Depends(get_db)]
class Credentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    email: EmailStr = Field(max_length=254)
    password: str = Field(min_length=12, max_length=128)
class RefreshInput(BaseModel):
    model_config = ConfigDict(extra='forbid')
    refreshToken: str = Field(pattern=r'^[A-Za-z0-9_-]{43}$')
class TokenPair(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str
    expiresIn: int
class UserOut(BaseModel):
    id: int
    email: str
@router.post('/register', response_model=UserOut, status_code=201, summary='로컬 회원가입')
def register(data: Credentials, db: DB):
    user = User(email=str(data.email).lower(), password_hash=password_hash(data.password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, 'EMAIL_EXISTS')
    return {'id': user.id, 'email': user.email}
@router.post('/login', response_model=TokenPair, summary='로그인 및 앱 토큰 발급')
def login(data: Credentials, db: DB):
    user = db.scalar(select(User).where(User.email == str(data.email).lower()))
    # 존재하지 않는 계정도 해시 계산을 수행하여 단순한 시간차 계정 추측을 줄인다.
    stored = user.password_hash if user and user.password_hash else password_hash('dummy-password-value')
    valid = password_matches(data.password, stored)
    if not user or not user.password_hash or not valid:
        raise HTTPException(401, 'LOGIN_FAILED')
    tokens = issue_tokens(db, user.id)
    db.commit()
    return tokens
def lock_refresh_owner(db, token_hash):
    # 사용자 row를 먼저 잠가 같은 사용자의 회전/로그아웃을 직렬화한다.
    owner = db.scalar(select(RefreshToken.user_id).where(RefreshToken.token_hash == token_hash))
    if owner is None:
        raise HTTPException(401, 'INVALID_REFRESH')
    db.execute(select(User.id).where(User.id == owner).with_for_update()).all()
    return db.scalar(select(RefreshToken).where(RefreshToken.token_hash == token_hash).with_for_update())
@router.post('/refresh', response_model=TokenPair, summary='리프레시 토큰 회전')
def refresh(data: RefreshInput, db: DB):
    old = lock_refresh_owner(db, digest(data.refreshToken))
    if old.revoked_at is not None or old.expires_at <= now():
        # 재사용된 이전 토큰을 발견하면 해당 family 전체를 폐기한다. 반드시 commit 후 401을 반환한다.
        db.execute(update(RefreshToken).where(RefreshToken.family_id == old.family_id).values(revoked_at=now()))
        db.commit()
        raise HTTPException(401, 'REFRESH_REUSED_OR_EXPIRED')
    old.revoked_at = now()
    # 회전해도 최초 로그인 세션의 7일 절대 만료는 연장하지 않는다.
    tokens = issue_tokens(db, old.user_id, old.family_id, old.expires_at)
    db.commit()
    return tokens
@router.post('/logout', status_code=204, summary='현재 로그인 세션의 리프레시 토큰 폐기')
def logout(data: RefreshInput, db: DB):
    token_hash = digest(data.refreshToken)
    if db.scalar(select(RefreshToken.id).where(RefreshToken.token_hash == token_hash)) is not None:
        old = lock_refresh_owner(db, token_hash)
        db.execute(update(RefreshToken).where(RefreshToken.family_id == old.family_id).values(revoked_at=now()))
        db.commit()
    # 서명된 access JWT는 15분 만료까지 유효하다. 즉시 폐기는 denylist/session 조회가 별도로 필요하다.
    return Response(status_code=204)
