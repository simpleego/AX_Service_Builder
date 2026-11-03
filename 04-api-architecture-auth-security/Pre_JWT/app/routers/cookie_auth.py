"""
[실습 1] 쿠키(Cookie) 기반 인증

  1-1. 평문 쿠키   (/cookie/v1/*) : 쿠키에 user_id를 그대로 저장  → 위조 가능! (취약점 체험용)
  1-2. 서명 쿠키   (/cookie/v2/*) : 쿠키 값에 서버 비밀키로 서명 → 위조 시 서명 검증 실패

핵심 개념
- 서버는 Set-Cookie 응답 헤더로 브라우저에 값을 저장시키고,
  브라우저는 이후 같은 사이트 요청마다 Cookie 헤더로 그 값을 자동 전송합니다.
- 쿠키 방식은 '로그인 상태 정보'를 클라이언트가 들고 있습니다. (서버는 상태를 저장하지 않음 = Stateless)
- 1-2의 '서명된 쿠키'는 이후 배울 JWT와 원리가 같습니다. (데이터 + 서명, 서버 저장소 없음)
"""
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from sqlalchemy.orm import Session

from app.config import COOKIE_SECURE, SECRET_KEY, SESSION_EXPIRE_MINUTES
from app.database import get_db
from app.models import User
from app.routers.users import authenticate_user
from app.schemas import LoginRequest, MessageResponse, UserResponse

router = APIRouter(prefix="/cookie", tags=["1. 쿠키 인증"])

MAX_AGE = SESSION_EXPIRE_MINUTES * 60  # 초 단위


# =====================================================================
# 1-1. 평문 쿠키 (취약한 방식 - 절대 실무에서 사용 금지)
# =====================================================================
@router.post("/v1/login", response_model=MessageResponse)
def login_plain(req: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.username, req.password)

    # 브라우저에 user_id=1 같은 값을 그대로 저장
    response.set_cookie(
        key="user_id",
        value=str(user.id),
        max_age=MAX_AGE,
        httponly=True,     # JavaScript(document.cookie)로 읽을 수 없게 → XSS 탈취 방어
        samesite="lax",    # 다른 사이트에서 보내는 요청에는 쿠키 전송 제한 → CSRF 완화
        secure=COOKIE_SECURE,  # True면 HTTPS에서만 전송
    )
    return {"message": f"[v1] {user.username}님 로그인 (쿠키 user_id={user.id})"}


@router.get("/v1/me", response_model=UserResponse)
def me_plain(
    db: Session = Depends(get_db),
    user_id: Annotated[str | None, Cookie()] = None,  # 'user_id' 쿠키를 자동으로 읽어옴
):
    """
    ⚠ 취약점: 쿠키 값을 user_id=2 로 바꿔서 보내면 2번 사용자로 로그인됩니다.
       (curl -b "user_id=2" http://localhost:8000/cookie/v1/me)
    """
    if user_id is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")
    user = db.get(User, int(user_id)) if user_id.isdigit() else None
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "유효하지 않은 쿠키입니다.")
    return user


@router.post("/v1/logout", response_model=MessageResponse)
def logout_plain(response: Response):
    response.delete_cookie("user_id")
    return {"message": "[v1] 로그아웃 (쿠키 삭제)"}


# =====================================================================
# 1-2. 서명된 쿠키 (Signed Cookie)
# =====================================================================
# SECRET_KEY로 HMAC 서명 + 생성 시각(timestamp)을 함께 기록
serializer = URLSafeTimedSerializer(SECRET_KEY, salt="cookie-auth")


@router.post("/v2/login", response_model=MessageResponse)
def login_signed(req: LoginRequest, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, req.username, req.password)

    # 결과 예: eyJ1aWQiOjEsInVuYW1lIjoiaG9uZyJ9.ZyXk1w.Qm0b...  (데이터.시각.서명)
    token = serializer.dumps({"uid": user.id, "uname": user.username})

    response.set_cookie(
        key="auth",
        value=token,
        max_age=MAX_AGE,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
    )
    return {"message": f"[v2] {user.username}님 로그인 (서명된 쿠키 발급)"}


def get_user_from_signed_cookie(
    db: Session = Depends(get_db),
    auth: Annotated[str | None, Cookie()] = None,
) -> User:
    """서명 쿠키 검증 의존성 - 보호가 필요한 API에 Depends로 붙여 사용"""
    if auth is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "로그인이 필요합니다.")
    try:
        # 서명 검증 + 만료(max_age) 검증을 동시에 수행
        data = serializer.loads(auth, max_age=MAX_AGE)
    except SignatureExpired:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "로그인이 만료되었습니다.")
    except BadSignature:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "위조되었거나 손상된 쿠키입니다.")

    user = db.get(User, data["uid"])
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "존재하지 않는 사용자입니다.")
    return user


@router.get("/v2/me", response_model=UserResponse)
def me_signed(user: User = Depends(get_user_from_signed_cookie)):
    return user


@router.get("/v2/inspect")
def inspect_signed_cookie(auth: Annotated[str | None, Cookie()] = None):
    """
    [학습용] 서명 쿠키의 내용은 '암호화'가 아니라 '인코딩'일 뿐이라는 것을 확인
    → 서명 없이도 누구나 내용을 읽을 수 있음 (변조만 막을 뿐, 비밀 정보는 넣으면 안 됨)
    """
    if auth is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "auth 쿠키가 없습니다. /cookie/v2/login 먼저 실행하세요.")
    import base64
    import json

    payload_b64 = auth.split(".")[0]
    payload_b64 += "=" * (-len(payload_b64) % 4)  # base64 패딩 보정
    decoded = json.loads(base64.urlsafe_b64decode(payload_b64))
    return {"raw_cookie": auth, "parts": auth.split("."), "decoded_payload(서명검증 없이 읽음)": decoded}


@router.post("/v2/logout", response_model=MessageResponse)
def logout_signed(response: Response):
    """
    ⚠ 한계: 쿠키를 지우라고 '요청'할 뿐, 서버는 이 토큰을 무효화할 방법이 없습니다.
       누군가 쿠키 값을 미리 복사해 두었다면 만료 시각까지 계속 사용할 수 있습니다.
       → 이 문제를 해결하는 것이 [실습 2] 서버 세션 방식입니다. (JWT도 같은 한계를 가짐)
    """
    response.delete_cookie("auth")
    return {"message": "[v2] 로그아웃 (브라우저 쿠키 삭제)"}
