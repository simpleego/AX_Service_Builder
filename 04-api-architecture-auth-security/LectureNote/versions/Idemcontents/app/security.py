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
