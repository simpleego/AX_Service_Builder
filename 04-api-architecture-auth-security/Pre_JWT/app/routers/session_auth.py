"""
[실습 2] 세션(Session) 기반 인증 - 서버 측 세션 저장소로 MySQL 사용

동작 흐름
  1) 로그인 성공 → 추측 불가능한 session_id 생성 → login_sessions 테이블에 저장
  2) Set-Cookie: session_id=<랜덤값>  (쿠키에는 아무 의미 없는 '열쇠 번호'만 저장)
  3) 이후 요청 → 브라우저가 session_id 쿠키 자동 전송
               → 서버가 DB에서 session_id 조회 → 사용자 식별
  4) 로그아웃 → DB에서 세션 행 삭제 → 즉시 무효화 (쿠키를 복사해 둔 사람도 사용 불가)

쿠키 방식과의 차이
  - 상태(누가 로그인했는지)를 '서버'가 관리 → Stateful
  - 강제 로그아웃, 동시 접속 관리, 접속 기기 목록 조회가 가능
  - 대신 매 요청마다 DB 조회가 필요 (실무에서는 보통 Redis 사용)
"""
import secrets
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, Response, status
from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.config import COOKIE_SECURE, SESSION_EXPIRE_MINUTES
from app.database import get_db
from app.models import LoginSession, User
from app.routers.users import authenticate_user
from app.schemas import LoginRequest, MessageResponse, SessionInfo, UserResponse

router = APIRouter(prefix="/session", tags=["2. 세션 인증"])

SESSION_COOKIE_NAME = "session_id"
SESSION_TTL = timedelta(minutes=SESSION_EXPIRE_MINUTES)


def _now() -> datetime:
    # MySQL DATETIME은 타임존 정보가 없으므로 naive datetime으로 통일
    return datetime.now()


def _set_session_cookie(response: Response, session_id: str) -> None:
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        max_age=int(SESSION_TTL.total_seconds()),
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
    )


# ---------------------------------------------------------------------
# 로그인 / 로그아웃
# ---------------------------------------------------------------------
@router.post("/login", response_model=MessageResponse)
def login(
    req: LoginRequest,
    request: Request,
    response: Response,
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, req.username, req.password)

    # 만료된 세션 정리 (실무에서는 스케줄러나 MySQL EVENT로 처리)
    db.execute(delete(LoginSession).where(LoginSession.expires_at < _now()))

    # 세션 ID: 암호학적으로 안전한 난수 (random 모듈 사용 금지!)
    # 로그인할 때마다 '새로' 발급 → 세션 고정(Session Fixation) 공격 방지
    session_id = secrets.token_urlsafe(32)
    now = _now()

    db.add(
        LoginSession(
            session_id=session_id,
            user_id=user.id,
            created_at=now,
            expires_at=now + SESSION_TTL,
            last_accessed_at=now,
            ip_address=request.client.host if request.client else None,
            user_agent=(request.headers.get("user-agent") or "")[:255],
        )
    )
    db.commit()

    _set_session_cookie(response, session_id)
    return {"message": f"{user.username}님 로그인 성공 (세션 생성)"}


# ---------------------------------------------------------------------
# 인증 의존성: 보호할 API에 Depends(get_current_user) 만 붙이면 됨
# ---------------------------------------------------------------------
def _find_valid_session(db: Session, session_id: str | None) -> LoginSession:
    """쿠키의 session_id로 DB에서 유효한 세션을 찾음 (없거나 만료면 401)"""
    if session_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")

    login_session = db.get(LoginSession, session_id)
    if login_session is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "유효하지 않은 세션입니다. 다시 로그인하세요.")

    if login_session.expires_at < _now():
        db.delete(login_session)
        db.commit()
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "세션이 만료되었습니다. 다시 로그인하세요.")

    return login_session


def get_current_session(
    response: Response,
    db: Session = Depends(get_db),
    session_id: Annotated[str | None, Cookie()] = None,
) -> LoginSession:
    login_session = _find_valid_session(db, session_id)

    # 슬라이딩 만료(Sliding Expiration): 활동할 때마다 만료 시각을 연장
    now = _now()
    login_session.last_accessed_at = now
    login_session.expires_at = now + SESSION_TTL
    db.commit()
    _set_session_cookie(response, session_id)  # 브라우저 쿠키 만료시각도 함께 연장

    return login_session


def get_current_user(login_session: LoginSession = Depends(get_current_session)) -> User:
    return login_session.user


# ---------------------------------------------------------------------
# 보호된 API 예시
# ---------------------------------------------------------------------
@router.get("/me", response_model=UserResponse)
def me(user: User = Depends(get_current_user)):
    """로그인한 사용자 정보"""
    return user


@router.get("/mypage")
def mypage(user: User = Depends(get_current_user)):
    """로그인해야만 볼 수 있는 페이지라고 가정"""
    return {"message": f"{user.username}님의 마이페이지입니다.", "email": user.email}


@router.get("/devices", response_model=list[SessionInfo])
def list_my_sessions(
    current: LoginSession = Depends(get_current_session),
    db: Session = Depends(get_db),
):
    """
    현재 로그인되어 있는 모든 기기(세션) 목록
    → 서버가 세션을 저장하기 때문에 가능한 기능 (쿠키/JWT 방식에서는 불가능)
    """
    rows = db.scalars(
        select(LoginSession)
        .where(LoginSession.user_id == current.user_id, LoginSession.expires_at >= _now())
        .order_by(LoginSession.created_at)
    ).all()
    return [
        SessionInfo(
            session_id=s.session_id[:8] + "...",  # 전체 세션 ID는 노출하지 않음
            created_at=s.created_at,
            expires_at=s.expires_at,
            last_accessed_at=s.last_accessed_at,
            ip_address=s.ip_address,
            user_agent=s.user_agent,
            is_current=(s.session_id == current.session_id),
        )
        for s in rows
    ]


@router.post("/logout", response_model=MessageResponse)
def logout(
    response: Response,
    db: Session = Depends(get_db),
    session_id: Annotated[str | None, Cookie()] = None,
):
    """현재 기기 로그아웃: DB에서 세션을 삭제 → 서버 측에서 즉시 무효화"""
    if session_id:
        db.execute(delete(LoginSession).where(LoginSession.session_id == session_id))
        db.commit()
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": "로그아웃 되었습니다. (세션 삭제)"}


@router.post("/logout-all", response_model=MessageResponse)
def logout_all(
    response: Response,
    db: Session = Depends(get_db),
    session_id: Annotated[str | None, Cookie()] = None,
):
    """모든 기기에서 로그아웃 (비밀번호 변경·계정 도용 의심 시 사용)"""
    current = _find_valid_session(db, session_id)  # 곧 삭제할 세션이므로 만료 연장은 하지 않음
    result = db.execute(delete(LoginSession).where(LoginSession.user_id == current.user_id))
    db.commit()
    response.delete_cookie(SESSION_COOKIE_NAME)
    return {"message": f"모든 기기에서 로그아웃 되었습니다. (삭제된 세션 {result.rowcount}개)"}
