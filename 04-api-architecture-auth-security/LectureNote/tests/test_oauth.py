"""Google 응답은 mock한다. 실제 Google 서명 검증/네트워크 연동 완료를 의미하지 않는다."""
import importlib
from urllib.parse import urlparse, parse_qs
import pytest
from sqlalchemy import select, func
from conftest import OAUTH, models
pytestmark = pytest.mark.skipif(not OAUTH, reason='v04 이상 Google 실습')

def begin(client):
    response = client.get('/api/auth/google', follow_redirects=False)
    assert response.status_code == 302
    params = parse_qs(urlparse(response.headers['location']).query)
    assert params['code_challenge_method'] == ['S256']
    assert 'HttpOnly' in response.headers['set-cookie']
    return params

def mock_google(monkeypatch, nonce, subject='google-test-subject'):
    oauth = importlib.import_module('app.oauth')
    class Reply:
        def raise_for_status(self): pass
        def json(self): return {'id_token':'mocked-google-id-token'}
    monkeypatch.setattr(oauth.httpx, 'post', lambda *args, **kwargs: Reply())
    monkeypatch.setattr(oauth.id_token, 'verify_oauth2_token', lambda *args, **kwargs:
        {'sub':subject,'nonce':nonce,'email':'student@example.com','email_verified':True})

def test_state_missing_binding_replay_and_nonce(client, monkeypatch):
    assert client.get('/api/auth/google/callback?state=wrong&code=wrong').status_code == 400
    params = begin(client)
    binding = client.cookies.get('oauth_binding')
    client.cookies.clear()
    path = '/api/auth/google/callback?state='+params['state'][0]+'&code=sample'
    assert client.get(path).status_code == 400
    client.cookies.set('oauth_binding', binding, domain='testserver.local', path='/api/auth/google')
    mock_google(monkeypatch, 'wrong-nonce')
    assert client.get(path).status_code == 401
    assert client.get(path).status_code == 400  # 실패해도 state는 소비되어 재사용 불가

def test_google_login_identity_and_no_email_merge(context, monkeypatch):
    client, factory = context
    with factory() as db:
        db.add(models.User(email='student@example.com', password_hash='local-placeholder'))
        db.commit()
    for _ in range(2):
        params = begin(client)
        mock_google(monkeypatch, params['nonce'][0])
        response = client.get('/api/auth/google/callback', params={'state':params['state'][0], 'code':'sample'})
        assert response.status_code == 200
        assert response.headers['cache-control'] == 'no-store'
        assert client.get('/api/todos', headers={'Authorization':'Bearer '+response.json()['accessToken']}).status_code == 200
    with factory() as db:
        assert db.scalar(select(func.count()).select_from(models.SocialAccount)) == 1
        account = db.scalar(select(models.SocialAccount))
        social = db.get(models.User, account.user_id)
        assert social.email is None  # 같은 이메일의 로컬 사용자를 인수하지 않았다.

def test_oauth_not_configured(client, monkeypatch):
    monkeypatch.delenv('GOOGLE_CLIENT_ID', raising=False)
    assert client.get('/api/auth/google', follow_redirects=False).status_code == 503
