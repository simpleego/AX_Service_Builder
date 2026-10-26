"""
📌 5일차 실습 — OAuth2 Authorization Code 흐름 (Google 예시)

⚠️ 실습 전 준비물
1. https://console.cloud.google.com 에서 OAuth 클라이언트 ID 발급
2. 승인된 리디렉션 URI에 http://localhost:8000/auth/oauth/google/callback 등록
3. app/core/config.py 의 GOOGLE_CLIENT_ID / SECRET 값을 본인 값으로 교체

강의안 5일차 시퀀스 다이어그램을 보면서 아래 두 단계를 구현하세요.
"""
from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.database import get_db
from app.repositories import user_repository
from app.services import auth_service

router = APIRouter(prefix="/auth/oauth", tags=["소셜 로그인"])

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


@router.get("/google/login")
def google_login():
    """
    TODO (1단계): 사용자를 구글 로그인·동의 화면으로 리다이렉트하세요.
    필요한 쿼리 파라미터: client_id, redirect_uri, response_type=code,
                        scope="openid email profile", access_type=offline
    힌트: RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")
    """
    raise NotImplementedError


@router.get("/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    """
    TODO (2단계):
    1. code를 구글 access_token으로 교환
       httpx.Client().post(GOOGLE_TOKEN_URL, data={code, client_id, client_secret, redirect_uri, grant_type})
    2. 받은 access_token으로 사용자 정보 조회 (GOOGLE_USERINFO_URL, Authorization 헤더)
    3. email로 기존 사용자 찾기 -> 없으면 자동 회원가입 (password_hash=None)
    4. auth_service.issue_tokens로 우리 서비스의 토큰 발급 후 반환

    💡 비밀번호는 절대 이 과정에 등장하지 않는다는 점을 확인하세요.
    """
    raise NotImplementedError
