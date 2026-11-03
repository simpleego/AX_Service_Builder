"""
회원가입 (쿠키/세션 실습 공통)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas import SignupRequest, UserResponse
from app.security import hash_password, verify_password

router = APIRouter(prefix="/users", tags=["0. 회원가입(공통)"])


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    """회원가입: 비밀번호는 bcrypt 해시로 변환하여 저장"""
    exists = db.scalar(
        select(User).where(or_(User.username == req.username, User.email == req.email))
    )
    if exists:
        raise HTTPException(status.HTTP_409_CONFLICT, "이미 사용 중인 아이디 또는 이메일입니다.")

    user = User(
        username=req.username,
        email=req.email,
        password_hash=hash_password(req.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, username: str, password: str) -> User:
    """
    아이디/비밀번호 확인 (쿠키·세션 로그인에서 공통 사용)
    - 아이디가 없을 때와 비밀번호가 틀릴 때 같은 메시지를 돌려줘
      '어떤 아이디가 존재하는지' 알아낼 수 없게 합니다.
    """
    user = db.scalar(select(User).where(User.username == username))
    if user is None or not verify_password(password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "아이디 또는 비밀번호가 올바르지 않습니다.")
    return user
