"""실제 MySQL이 없어도 HTTP/보안 규칙을 검사하는 SQLite 대체 테스트 DB.

MySQL의 DDL, 행 잠금, 동시성 검증을 대체하지 않는다. 실 DB 검증은 Postman으로 수행한다.
"""
import os, sys, importlib
from pathlib import Path
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
ROOT = Path(__file__).resolve().parents[1]
VERSION = os.getenv('TEST_VERSION', 'v06-postman')
os.environ['JWT_SECRET'] = 'test-only-secret-0123456789-abcdefghijklmnopqrstuvwxyz'
os.environ['GOOGLE_CLIENT_ID'] = 'test-google-client'
os.environ['GOOGLE_CLIENT_SECRET'] = 'test-google-secret'
sys.path.insert(0, str(ROOT/'versions'/VERSION))
main = importlib.import_module('app.main')
database = importlib.import_module('app.database')
models = importlib.import_module('app.models')
STAGE = 7 if VERSION == 'Idemcontents' else int(VERSION[1:3])
AUTH = STAGE >= 3
OAUTH = STAGE >= 4
@pytest.fixture
def context(monkeypatch):
    engine = create_engine('sqlite://', connect_args={'check_same_thread':False}, poolclass=StaticPool)
    models.Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as db:
        db.add(models.User(id=1, email='classroom@example.invalid', password_hash=None))
        db.commit()
    def override_db():
        with factory() as db:
            try:
                yield db
            except Exception:
                db.rollback()
                raise
    main.app.dependency_overrides[database.get_db] = override_db
    monkeypatch.setattr(main, 'engine', engine)
    # context manager로 startup/health/shutdown까지 대체 DB에서 실행한다.
    with TestClient(main.app) as client:
        yield client, factory
    main.app.dependency_overrides.clear()
    engine.dispose()
@pytest.fixture
def client(context):
    return context[0]
def signup(client, email='student@example.com'):
    credentials = {'email':email, 'password':'Classroom-Only-12345!'}
    assert client.post('/api/auth/register', json=credentials).status_code == 201
    response = client.post('/api/auth/login', json=credentials)
    assert response.status_code == 200
    return response.json(), credentials
@pytest.fixture
def tokens(client):
    if not AUTH:
        return {}
    return signup(client)[0]
@pytest.fixture
def headers(tokens):
    return {'Authorization':'Bearer '+tokens['accessToken']} if AUTH else {}
