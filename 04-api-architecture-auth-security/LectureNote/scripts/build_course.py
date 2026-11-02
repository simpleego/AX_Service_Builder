"""한국어 주석이 포함된 독립 FastAPI 실습 스냅샷을 생성한다. 실행하면 versions 소스를 갱신한다."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
VERSIONS = ['v01-rest', 'v02-spec', 'v03-jwt', 'v04-oauth', 'v05-layered-swagger', 'v06-postman']
def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip() + '\n', encoding='utf-8')

DATABASE = '''
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
load_dotenv()
# URL.create는 비밀번호의 @, / 등 특수문자를 안전하게 인코딩한다.
url = URL.create('mysql+pymysql', username=os.getenv('DB_USER', 'todo_app'),
    password=os.getenv('DB_PASSWORD', ''), host=os.getenv('DB_HOST', 'localhost'),
    port=int(os.getenv('DB_PORT', '3306')), database=os.getenv('DB_NAME', 'todo_course'),
    query={'charset': 'utf8mb4'})
engine = create_engine(url, pool_pre_ping=True, pool_recycle=1800)
@event.listens_for(engine, 'connect')
def set_utc(connection, _record):
    # DB/서버의 로컬 시간대가 달라도 토큰 만료 계산은 UTC로 통일한다.
    with connection.cursor() as cursor:
        cursor.execute("SET time_zone = '+00:00'")
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
def get_db():
    # 요청마다 세션을 만들고 예외 시 롤백한다. 트랜잭션 경계는 서비스에서 결정한다.
    with SessionLocal() as db:
        try:
            yield db
        except Exception:
            db.rollback()
            raise
'''

MODELS = '''
from datetime import datetime
from sqlalchemy import String, Integer, Boolean, DateTime, ForeignKey, text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
class Base(DeclarativeBase):
    pass
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str | None] = mapped_column(String(254), unique=True)
    password_hash: Mapped[str | None] = mapped_column(String(200))
class Todo(Base):
    __tablename__ = 'todos'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    title: Mapped[str] = mapped_column(String(200))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))
class RefreshToken(Base):
    __tablename__ = 'refresh_tokens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    family_id: Mapped[str] = mapped_column(String(36))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime)
class SocialAccount(Base):
    __tablename__ = 'social_accounts'
    __table_args__ = (UniqueConstraint('provider', 'provider_subject'),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    provider: Mapped[str] = mapped_column(String(30))
    provider_subject: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    provider_email: Mapped[str | None] = mapped_column(String(254))
class OAuthState(Base):
    __tablename__ = 'oauth_states'
    state_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    binding_hash: Mapped[str] = mapped_column(String(64))
    nonce: Mapped[str] = mapped_column(String(64))
    verifier: Mapped[str] = mapped_column(String(128))
    expires_at: Mapped[datetime] = mapped_column(DateTime)
# 테이블 생성은 database/01-schema.sql을 기준으로 한다. 앱이 DDL 권한을 갖지 않도록 create_all은 호출하지 않는다.
'''

SCHEMAS = '''
from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
class TodoCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: Title
    completed: bool = Field(default=False, strict=True)
class TodoPatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: Title | None = None
    completed: bool | None = Field(default=None, strict=True)
    @model_validator(mode='after')
    def check_patch(self):
        # PATCH는 전달한 필드만 바꾼다. 빈 객체/명시적 null은 허용하지 않는다.
        if not self.model_fields_set or any(getattr(self, k) is None for k in self.model_fields_set):
            raise ValueError('하나 이상의 title/completed 필드를 null 없이 입력하세요.')
        return self
class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
class TodoPage(BaseModel):
    data: list[TodoOut]
    page: int
    limit: int
'''

REPOSITORY = '''
from sqlalchemy import select
from sqlalchemy.orm import Session
from .models import Todo
class TodoRepository:
    def __init__(self, db: Session):
        self.db = db
    def list(self, owner: int, page: int, limit: int, completed: bool | None):
        query = select(Todo).where(Todo.owner_id == owner)
        if completed is not None:
            query = query.where(Todo.completed == completed)
        # SQLAlchemy가 입력값을 바인딩하므로 문자열 결합 SQL을 작성하지 않는다.
        return self.db.scalars(query.order_by(Todo.id.desc()).offset((page-1)*limit).limit(limit)).all()
    def find(self, owner: int, todo_id: int):
        # 상세/수정/삭제 모두 소유권을 SQL 조건에 넣어 IDOR를 방지한다.
        return self.db.scalar(select(Todo).where(Todo.id == todo_id, Todo.owner_id == owner))
    def add(self, owner: int, values: dict):
        todo = Todo(owner_id=owner, **values)
        self.db.add(todo)
        return todo
'''

SERVICE = '''
from fastapi import HTTPException
from .todo_repository import TodoRepository
from .schemas import TodoCreate, TodoPatch
class TodoService:
    def __init__(self, db):
        self.db, self.repo = db, TodoRepository(db)
    def list(self, owner, page, limit, completed):
        return {'data': self.repo.list(owner, page, limit, completed), 'page': page, 'limit': limit}
    def get(self, owner, todo_id):
        todo = self.repo.find(owner, todo_id)
        if todo is None:
            # 타인의 Todo와 없는 Todo에 같은 404를 주어 존재 여부를 숨긴다.
            raise HTTPException(404, 'TODO_NOT_FOUND')
        return todo
    def create(self, owner, data: TodoCreate):
        todo = self.repo.add(owner, data.model_dump())
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def update(self, owner, todo_id, data: TodoPatch):
        todo = self.get(owner, todo_id)
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(todo, key, value)
        self.db.commit()
        self.db.refresh(todo)
        return todo
    def remove(self, owner, todo_id):
        self.db.delete(self.get(owner, todo_id))
        self.db.commit()
'''

CONTROLLER = '''
from typing import Annotated
from fastapi import APIRouter, Depends, Query, Path, Response
from sqlalchemy.orm import Session
from .database import get_db
from .schemas import TodoCreate, TodoPatch, TodoOut, TodoPage
from .todo_service import TodoService
from .identity import current_user
router = APIRouter(prefix='/api/todos', tags=['Todos'])
DB = Annotated[Session, Depends(get_db)]
Owner = Annotated[int, Depends(current_user)]
TodoId = Annotated[int, Path(gt=0, le=4294967295)]
# 컨트롤러는 HTTP 계약을, 서비스는 업무/트랜잭션을, 저장소는 데이터 조회를 담당한다.
@router.get('', response_model=TodoPage, summary='내 할 일 목록')
def list_todos(db: DB, owner: Owner, page: int = Query(1, ge=1, le=1000000),
               limit: int = Query(20, ge=1, le=100), completed: bool | None = None):
    return TodoService(db).list(owner, page, limit, completed)
@router.post('', response_model=TodoOut, status_code=201, summary='할 일 생성')
def create_todo(data: TodoCreate, response: Response, db: DB, owner: Owner):
    todo = TodoService(db).create(owner, data)
    response.headers['Location'] = f'/api/todos/{todo.id}'
    return todo
@router.get('/{todo_id}', response_model=TodoOut, summary='내 할 일 상세')
def get_todo(todo_id: TodoId, db: DB, owner: Owner):
    return TodoService(db).get(owner, todo_id)
@router.patch('/{todo_id}', response_model=TodoOut, summary='할 일 일부 수정')
def update_todo(todo_id: TodoId, data: TodoPatch, db: DB, owner: Owner):
    return TodoService(db).update(owner, todo_id, data)
@router.delete('/{todo_id}', status_code=204, summary='할 일 삭제')
def delete_todo(todo_id: TodoId, db: DB, owner: Owner):
    TodoService(db).remove(owner, todo_id)
    return Response(status_code=204)
'''

SECURITY = '''
import os, secrets, hashlib, hmac, base64, uuid
from datetime import datetime, timedelta, timezone
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .models import RefreshToken
SECRET = os.getenv('JWT_SECRET', '')
if len(SECRET.encode()) < 32:
    raise RuntimeError('JWT_SECRET에 무작위 32바이트 이상의 비밀값을 지정하세요.')
ISSUER, AUDIENCE = 'todo-api', 'todo-client'
def now():
    # MySQL DATETIME은 timezone 정보가 없으므로 UTC naive datetime으로 통일한다.
    return datetime.now(timezone.utc).replace(tzinfo=None)
def digest(value: str):
    return hashlib.sha256(value.encode()).hexdigest()
def password_hash(password: str, salt: str | None = None):
    salt = salt or secrets.token_hex(16)
    # 사용자별 salt와 scrypt로 비밀번호를 단방향 해시한다. DB에는 평문을 저장하지 않는다.
    hashed = hashlib.scrypt(password.encode(), salt=salt.encode(), n=16384, r=8, p=1, dklen=64)
    return salt + ':' + hashed.hex()
def password_matches(password, stored):
    return bool(stored) and hmac.compare_digest(password_hash(password, stored.split(':')[0]), stored)
def issue_tokens(db, user_id: int, family: str | None = None, expires: datetime | None = None):
    stamp = now()
    access = jwt.encode({'sub': str(user_id), 'type': 'access', 'iss': ISSUER, 'aud': AUDIENCE,
        'iat': stamp.replace(tzinfo=timezone.utc), 'exp': (stamp+timedelta(minutes=15)).replace(tzinfo=timezone.utc)}, SECRET, algorithm='HS256')
    refresh = secrets.token_urlsafe(32)
    # opaque refresh token은 256비트 무작위 값이며 SHA-256 해시만 DB에 보관한다.
    db.add(RefreshToken(token_hash=digest(refresh), user_id=user_id, family_id=family or str(uuid.uuid4()),
        expires_at=expires or stamp+timedelta(days=7)))
    return {'accessToken': access, 'refreshToken': refresh, 'tokenType': 'Bearer', 'expiresIn': 900}
bearer = HTTPBearer(auto_error=False)
def current_user(credentials: HTTPAuthorizationCredentials | None = Depends(bearer)):
    try:
        if credentials is None:
            raise ValueError('missing bearer')
        # 서명뿐 아니라 알고리즘/issuer/audience/필수 claim/만료/토큰 종류까지 검증한다.
        payload = jwt.decode(credentials.credentials, SECRET, algorithms=['HS256'], issuer=ISSUER,
            audience=AUDIENCE, options={'require': ['exp', 'iat', 'sub', 'iss', 'aud', 'type']})
        if payload['type'] != 'access' or not payload['sub'].isdigit() or not 0 < int(payload['sub']) <= 4294967295:
            raise ValueError('invalid subject/type')
        return int(payload['sub'])
    except (jwt.PyJWTError, ValueError, KeyError, TypeError, AttributeError):
        raise HTTPException(401, 'UNAUTHORIZED', headers={'WWW-Authenticate': 'Bearer'})
'''

AUTH = '''
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
'''

OAUTH = '''
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
'''

MAIN = '''
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy import text
from .database import engine
from .todos import router as todo_router
@asynccontextmanager
async def lifespan(_app):
    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    yield
    engine.dispose()
app = FastAPI(title='Todo API - API 아키텍처 & 인증 보안', version='VERSION',
    description='48시간 단계별 실습. 인증과 Todo 소유권을 Postman으로 검증합니다.',
    docs_url=DOCS, redoc_url=None, openapi_url=OPENAPI, lifespan=lifespan)
@app.exception_handler(StarletteHTTPException)
async def http_error(_request: Request, exc):
    return JSONResponse({'error': {'code': str(exc.detail)}}, status_code=exc.status_code, headers=exc.headers)
@app.exception_handler(RequestValidationError)
async def validation_error(_request: Request, exc):
    # 검증 오류에 비밀번호 등 입력 원문을 포함하지 않는다.
    fields = [{'loc': list(e['loc']), 'type': e['type'], 'message': e['msg']} for e in exc.errors()]
    return JSONResponse({'error': {'code': 'VALIDATION_ERROR', 'fields': fields}}, status_code=422)
@app.exception_handler(Exception)
async def internal_error(_request: Request, _exc):
    return JSONResponse({'error': {'code': 'INTERNAL_ERROR'}}, status_code=500)
@app.middleware('http')
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['Referrer-Policy'] = 'no-referrer'
    if request.url.path.startswith('/api/auth'):
        response.headers['Cache-Control'] = 'no-store'
    return response
@app.get('/health', tags=['Health'], summary='DB 연결 확인')
def health():
    with engine.connect() as connection:
        connection.execute(text('SELECT 1'))
    return {'status': 'ok'}
app.include_router(todo_router)
'''

ENV = '''# .env로 복사 후 채우세요. 실제 비밀값은 Git에 커밋하지 않습니다.
DB_HOST=localhost
DB_PORT=3306
DB_NAME=todo_course
DB_USER=todo_app
DB_PASSWORD=ReplaceWithYourDatabasePassword
# v03 이상 필수: python -c "import secrets; print(secrets.token_urlsafe(48))"
JWT_SECRET=
# v04 이상 선택. Google 웹 애플리케이션 OAuth 클라이언트
GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
APP_ENV=development
'''
REQUIREMENTS = '''fastapi>=0.115,<1
uvicorn>=0.34,<1
SQLAlchemy>=2.0.38,<2.1
PyMySQL[rsa]>=1.1.1,<2
python-dotenv>=1.0.1,<2
pydantic[email]>=2.10,<3
'''
LABS = [
'''## 실습 목표 · REST (8H)
1. database.py의 get_db와 models.py의 User/Todo 관계를 읽고 /health를 호출합니다.
2. schemas.py에서 제목/완료 여부의 제약을 확인합니다.
3. todos.py에서 POST → GET 목록 → 상세 → PATCH → DELETE 순서로 구현을 따라갑니다.
4. Postman 01 폴더를 실행하고 201의 Location과 204의 빈 본문을 확인합니다.
5. page/limit/completed 쿼리를 바꾸고 빈 제목/잘못된 ID를 테스트합니다.

완료 기준: CRUD 5개 경로가 동작하고 소스의 owner_id=1 고정이 학습용임을 설명할 수 있습니다.
''',
'''## 실습 목표 · API 스펙 (6H)
1. docs/03-api-contract.md의 R01~R04를 자연어에서 요청/응답 표로 변환합니다.
2. v01 main.py와 비교하여 openapi_url 활성화를 확인합니다.
3. GET /openapi.json으로 paths와 components.schemas를 읽습니다.
4. title 최대 길이를 변경하면 DTO 검증과 명세가 함께 바뀌는지 확인합니다.
5. Postman에서 OpenAPI import를 해보고 제공 컬렉션과 상태코드를 비교합니다.

완료 기준: 입력/출력/필수값/상태코드/오류를 다른 팀이 구현할 수 있게 설명합니다.
''',
'''## 실습 목표 · JWT (12H)
1. security.py의 scrypt 해시와 password_matches를 먼저 읽습니다.
2. auth.py에서 register/login을 구현하고 DB에 평문이 없는지 확인합니다.
3. identity.py가 JWT current_user를 사용하도록 바뀐 점을 비교합니다.
4. A/B 사용자를 만들고 같은 Todo ID로 조회/수정/삭제해 소유권을 확인합니다.
5. refresh 정상 회전 → 이전 토큰 재사용 → 새 토큰 거부를 순서대로 관찰합니다.
6. logout 이후 refresh와 access의 유효성이 다른 이유를 설명합니다.

완료 기준: Postman 02 폴더 통과와 비밀/원문 토큰을 DB·로그에 남기지 않는 설계를 설명합니다.
''',
'''## 실습 목표 · OAuth2/OIDC (8H)
1. docs/04-auth-oauth.md에 따라 Google 웹 클라이언트와 redirect URI를 설정합니다.
2. oauth.py의 로그인 시작에서 state/nonce/verifier/binding의 차이를 확인합니다.
3. 브라우저로 로그인하고 callback의 앱 JWT를 Postman 환경에 복사합니다.
4. Postman 03 폴더로 소셜 사용자 Todo를 확인합니다.
5. 잘못된 state, 동의 취소, callback 재호출을 테스트합니다.
6. provider+sub로 식별하고 이메일로 자동 병합하지 않는 이유를 설명합니다.

완료 기준: Google 토큰과 앱 토큰의 역할을 구분하고 브라우저 로그인부터 Todo까지 연결합니다.
''',
'''## 실습 목표 · 계층/Swagger (8H)
1. v04의 todos.py와 v05의 세 파일을 나란히 비교합니다.
2. TodoRepository에는 SQL, TodoService에는 업무/commit, todos.py에는 HTTP 책임을 둡니다.
3. Depends(get_db), Depends(current_user)의 요청 흐름을 그립니다.
4. /docs에서 가입/로그인하고 Authorize 후 Todo CRUD를 호출합니다.
5. Postman 02 폴더를 다시 실행하여 구조 변경 뒤 동작이 같은지 확인합니다.

완료 기준: Controller→Service→Repository 호출 흐름과 트랜잭션 책임을 설명합니다.
''',
'''## 실습 목표 · Postman 통합 검증 (6H)
1. Postman 컬렉션/환경을 import하고 토큰/ID 저장 스크립트를 확인합니다.
2. 02 폴더를 개별 Send 후 Runner로 순서 실행합니다.
3. A/B 소유권, 잘못된 입력, refresh 재사용/로그아웃을 검증합니다.
4. docs/05-postman.md의 추가 수동 테스트를 수행합니다.
5. 루트 tests/로 자동 검증하고 대체 DB와 MySQL 검증의 차이를 기록합니다.

완료 기준: 성공/실패 시나리오와 예상 상태코드를 포함한 재현 가능한 검증 결과를 제출합니다.
''']
for i, name in enumerate(VERSIONS, 1):
    base = ROOT/'versions'/name
    write(base/'app/__init__.py', '# 이 폴더를 Python 패키지로 선언한다.')
    for filename, content in [('database.py', DATABASE), ('models.py', MODELS), ('schemas.py', SCHEMAS)]:
        write(base/'app'/filename, content)
    req = REQUIREMENTS
    if i >= 3:
        req += 'PyJWT>=2.10.1,<3\n'
        write(base/'app/security.py', SECURITY)
        write(base/'app/auth.py', AUTH)
        write(base/'app/identity.py', '# 인증 의존성을 라우터와 분리한다.\nfrom .security import current_user')
    else:
        write(base/'app/identity.py', '# v01~v02는 로그인 없이 공용 실습 계정 1번을 쓴다. 외부 공개 금지.\ndef current_user():\n    return 1')
    if i >= 4:
        req += 'httpx>=0.28.1,<1\ngoogle-auth>=2.38,<3\nrequests>=2.32.3,<3\n'
        write(base/'app/oauth.py', OAUTH)
    if i >= 5:
        for filename, content in [('todo_repository.py', REPOSITORY), ('todo_service.py', SERVICE), ('todos.py', CONTROLLER)]:
            write(base/'app'/filename, content)
    else:
        # 계층 분리 전에는 동일 동작을 한 파일에서 읽고 v05에서 역할별 파일로 추출한다.
        service = SERVICE.replace('from .todo_repository import TodoRepository\n', '')
        controller = CONTROLLER.replace('from .todo_service import TodoService\n', '')
        write(base/'app/todos.py', REPOSITORY+'\n'+service+'\n'+controller)
    main = MAIN.replace('VERSION', f'{i}.0.0').replace('DOCS', "'/docs'" if i >= 5 else 'None').replace('OPENAPI', "'/openapi.json'" if i >= 2 else 'None')
    if i >= 3: main += '\nfrom .auth import router as auth_router\napp.include_router(auth_router)\n'
    if i >= 4: main += '\nfrom .oauth import router as oauth_router\napp.include_router(oauth_router)\n'
    write(base/'app/main.py', main)
    write(base/'requirements.txt', req)
    write(base/'.env.example', ENV)
    write(base/'README.md', f'''# {name}

{i}단계 독립 실행 소스입니다. 공통 DB 준비는 ../../docs/02-database.md를 따릅니다.

```powershell
cd versions/{name}
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt
Copy-Item .env.example .env
# .env의 DB_PASSWORD와 v03 이상 JWT_SECRET을 채운다.
.venv/Scripts/python -m uvicorn app.main:app --reload --port 8000
```

macOS/Linux에서는 `.venv/bin/python`을 사용합니다. 반드시 이 버전 폴더에서 실행하세요.
다른 버전을 실행하기 전에 이전 서버를 Ctrl+C로 종료하세요.
v01~v02는 owner_id=1 고정이고, v03부터는 JWT 사용자만 자신의 Todo를 조회합니다.
v01에서 만든 Todo가 v03 신규 사용자에게 보이지 않는 것은 정상입니다.
DB는 한 번 준비하면 전 버전이 공유합니다. 버전 간 데이터 비교에는 다른 DB 이름을 사용할 수도 있습니다.
\n{LABS[i-1]}
''')
print('Generated six standalone FastAPI versions.')
