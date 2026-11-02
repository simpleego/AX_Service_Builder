"""JWT 검증과 DB에 남는 refresh 폐기 결과를 검증한다."""
import importlib
from datetime import timedelta, timezone
import pytest
from sqlalchemy import select
from conftest import AUTH, models
pytestmark = pytest.mark.skipif(not AUTH, reason='v03 이상 인증 실습')

def test_register_login_errors(client, tokens):
    credentials = {'email':'student@example.com','password':'Classroom-Only-12345!'}
    assert client.post('/api/auth/register', json=credentials).status_code == 409
    bad = client.post('/api/auth/login', json={**credentials,'password':'incorrect-password!'})
    assert bad.status_code == 401
    response = client.post('/api/auth/register', json={'email':'wrong','password':'short'})
    assert response.status_code == 422
    # 오류 type 이름(string_too_short)이 아니라 입력값 필드의 유무를 검사한다.
    assert all('input' not in field for field in response.json()['error']['fields'])

def test_password_and_refresh_storage(context, tokens):
    client, factory = context
    security = importlib.import_module('app.security')
    with factory() as db:
        user = db.scalar(select(models.User).where(models.User.email=='student@example.com'))
        assert user.password_hash != 'Classroom-Only-12345!'
        assert security.password_matches('Classroom-Only-12345!', user.password_hash)
        row = db.scalar(select(models.RefreshToken))
        assert row.token_hash == security.digest(tokens['refreshToken'])
        assert row.token_hash != tokens['refreshToken']

@pytest.mark.parametrize('case',['expired','wrong_audience','wrong_issuer','wrong_type','wrong_signature','missing_exp'])
def test_invalid_jwt(client, tokens, case):
    import jwt
    s = importlib.import_module('app.security')
    stamp = s.now().replace(tzinfo=timezone.utc)
    claims = {'sub':'2','type':'access','iss':s.ISSUER,'aud':s.AUDIENCE,'iat':stamp,'exp':stamp+timedelta(minutes=15)}
    secret = s.SECRET
    if case=='expired': claims['exp'] = stamp-timedelta(seconds=1)
    if case=='wrong_audience': claims['aud'] = 'other'
    if case=='wrong_issuer': claims['iss'] = 'other'
    if case=='wrong_type': claims['type'] = 'refresh'
    if case=='wrong_signature': secret = 'another-long-secret-012345678901234567890'
    if case=='missing_exp': del claims['exp']
    token = jwt.encode(claims, secret, algorithm='HS256')
    assert client.get('/api/todos', headers={'Authorization':'Bearer '+token}).status_code == 401

def test_refresh_rotation_reuse_revokes_family(context, tokens):
    client, factory = context
    old = tokens['refreshToken']
    response = client.post('/api/auth/refresh', json={'refreshToken':old})
    assert response.status_code == 200
    new = response.json()['refreshToken']
    assert new != old
    with factory() as db:
        rows = db.scalars(select(models.RefreshToken).order_by(models.RefreshToken.id)).all()
        assert len(rows)==2 and rows[0].revoked_at is not None
        assert rows[1].expires_at == rows[0].expires_at
    assert client.post('/api/auth/refresh', json={'refreshToken':old}).status_code == 401
    assert client.post('/api/auth/refresh', json={'refreshToken':new}).status_code == 401
    with factory() as db:
        assert all(x.revoked_at is not None for x in db.scalars(select(models.RefreshToken)).all())

def test_logout_and_expired_refresh(context, tokens, headers):
    client, factory = context
    s = importlib.import_module('app.security')
    assert client.post('/api/auth/logout', json={'refreshToken':tokens['refreshToken']}).status_code == 204
    assert client.post('/api/auth/refresh', json={'refreshToken':tokens['refreshToken']}).status_code == 401
    assert client.get('/api/todos', headers=headers).status_code == 200
    assert client.post('/api/auth/refresh', json={'refreshToken':'x'*43}).status_code == 401
    login = client.post('/api/auth/login', json={'email':'student@example.com','password':'Classroom-Only-12345!'}).json()
    with factory() as db:
        row = db.scalar(select(models.RefreshToken).where(models.RefreshToken.token_hash==s.digest(login['refreshToken'])))
        row.expires_at = s.now()-timedelta(seconds=1)
        db.commit()
    assert client.post('/api/auth/refresh', json={'refreshToken':login['refreshToken']}).status_code == 401
