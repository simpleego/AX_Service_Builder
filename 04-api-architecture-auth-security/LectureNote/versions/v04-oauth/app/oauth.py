import os, secrets, base64, hashlib
from datetime import timedelta
from urllib.parse import urlencode
from typing import Annotated
import httpx
from google.oauth2 import id_token
from google.auth.transport.requests import Request as GoogleRequest
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .database import get_db
from .models import OAuthState, SocialAccount, User
from .security import now, digest, issue_tokens
from .auth import TokenPair
router = APIRouter(prefix='/api/auth/google', tags=['Google OIDC'])
DB = Annotated[Session, Depends(get_db)]
CALLBACK = os.getenv('GOOGLE_REDIRECT_URI', 'http://localhost:8000/api/auth/google/callback')
COOKIE_PATH = '/api/auth/google'
def settings():
    client_id, secret = os.getenv('GOOGLE_CLIENT_ID'), os.getenv('GOOGLE_CLIENT_SECRET')
    if not client_id or not secret:
        raise HTTPException(503, 'OAUTH_NOT_CONFIGURED')
    return client_id, secret
@router.get('', summary='브라우저에서 Google 로그인 시작', responses={302: {'description': 'Google로 이동'}})
def google_start(db: DB):
    client_id, _ = settings()
    state, nonce, verifier, binding = [secrets.token_urlsafe(32) for _ in range(4)]
    # 서버 state와 브라우저 HttpOnly 쿠키를 함께 검증해 로그인 CSRF를 차단한다.
    db.add(OAuthState(state_hash=digest(state), binding_hash=digest(binding), nonce=nonce,
        verifier=verifier, expires_at=now()+timedelta(minutes=10)))
    db.commit()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    params = {'client_id': client_id, 'redirect_uri': CALLBACK, 'response_type': 'code',
        'scope': 'openid email profile', 'state': state, 'nonce': nonce,
        'code_challenge': challenge, 'code_challenge_method': 'S256'}
    response = RedirectResponse('https://accounts.google.com/o/oauth2/v2/auth?' + urlencode(params), status_code=302)
    response.set_cookie('oauth_binding', binding, max_age=600, httponly=True, samesite='lax',
        secure=os.getenv('APP_ENV') == 'production', path=COOKIE_PATH)
    return response
@router.get('/callback', response_model=TokenPair, summary='Google 인가 코드 교환 및 앱 JWT 발급')
def google_callback(request: Request, db: DB, state: str = '', code: str = '', error: str = ''):
    client_id, secret = settings()
    binding = request.cookies.get('oauth_binding', '')
    record = db.scalar(select(OAuthState).where(OAuthState.state_hash == digest(state),
        OAuthState.binding_hash == digest(binding), OAuthState.expires_at > now()).with_for_update())
    if not state or not binding or record is None:
        raise HTTPException(400, 'INVALID_STATE')
    nonce, verifier = record.nonce, record.verifier
    db.delete(record)
    db.commit()  # 외부 네트워크 요청 전에 일회성 state 소비를 확정한다.
    if error or not code:
        raise HTTPException(400, 'OAUTH_DENIED')
    try:
        # PKCE verifier는 브라우저에 노출하지 않고 서버에서만 사용한다.
        result = httpx.post('https://oauth2.googleapis.com/token', data={
            'client_id': client_id, 'client_secret': secret, 'code': code, 'code_verifier': verifier,
            'grant_type': 'authorization_code', 'redirect_uri': CALLBACK}, timeout=10)
        result.raise_for_status()
        profile = id_token.verify_oauth2_token(result.json()['id_token'], GoogleRequest(), client_id)
        # Google 라이브러리가 서명/issuer/audience/exp를 검증한다. nonce는 직접 비교한다.
        if profile.get('nonce') != nonce or not profile.get('sub'):
            raise ValueError('invalid nonce/sub')
    except Exception:
        raise HTTPException(401, 'OAUTH_FAILED')
    subject = profile['sub']
    account = db.scalar(select(SocialAccount).where(SocialAccount.provider == 'google', SocialAccount.provider_subject == subject))
    if account is None:
        # 이메일 일치만으로 로컬 계정에 자동 연결하지 않는다. provider + sub가 외부 신원이다.
        user = User(email=None, password_hash=None)
        db.add(user)
        db.flush()
        account = SocialAccount(provider='google', provider_subject=subject, user_id=user.id,
            provider_email=profile.get('email') if profile.get('email_verified') else None)
        db.add(account)
        try:
            db.commit()
        except IntegrityError:
            # 동시 최초 로그인은 UNIQUE 제약으로 중복 생성을 막고 기존 연결을 읽는다.
            db.rollback()
            account = db.scalar(select(SocialAccount).where(SocialAccount.provider == 'google', SocialAccount.provider_subject == subject))
            if account is None:
                raise
    tokens = issue_tokens(db, account.user_id)
    db.commit()
    # 프런트 없는 수업용 JSON 응답. 토큰을 URL에 넣지 않고 Google 토큰과 앱 JWT를 구분한다.
    response = JSONResponse(tokens)
    response.delete_cookie('oauth_binding', path=COOKIE_PATH)
    return response
