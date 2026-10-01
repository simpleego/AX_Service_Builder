"""API와 집계 논리 검증. SQLite 어댑터이므로 MariaDB 통합검증과 구분합니다."""
import sqlite3
from contextlib import contextmanager
from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main


class Cursor:
    def __init__(self, connection):
        self.raw = connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.raw.close()

    def execute(self, sql, parameters=()):
        return self.raw.execute(sql.replace('%s', '?').replace(' FOR UPDATE', ''), parameters)

    @property
    def lastrowid(self):
        return self.raw.lastrowid

    @property
    def rowcount(self):
        return self.raw.rowcount

    def fetchone(self):
        row = self.raw.fetchone()
        return dict(row) if row is not None else None

    def fetchall(self):
        return [dict(row) for row in self.raw.fetchall()]


class Connection:
    def __init__(self, raw):
        self.raw = raw

    def cursor(self):
        return Cursor(self.raw)


def sqlite_factory(path):
    @contextmanager
    def connect():
        raw = sqlite3.connect(path)
        raw.row_factory = sqlite3.Row
        raw.create_function('LOCATE', 2, lambda needle, haystack: haystack.casefold().find(needle.casefold()) + 1)
        try:
            yield Connection(raw)
            raw.commit()
        except Exception:
            raw.rollback()
            raise
        finally:
            raw.close()
    return connect


def initialize(path):
    with sqlite3.connect(path) as connection:
        connection.execute('''CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL, department TEXT NOT NULL,
            korean INTEGER NOT NULL, english INTEGER NOT NULL, math INTEGER NOT NULL
        )''')


@pytest.fixture
def client(tmp_path, monkeypatch):
    path = tmp_path / 'test.sqlite'
    initialize(path)
    monkeypatch.setattr(main, 'connect_db', sqlite_factory(path))
    with TestClient(main.app) as test_client:
        yield test_client


@pytest.mark.parametrize('score,grade', [(0,'F'),(59,'F'),(60,'D'),(69,'D'),(70,'C'),(79,'C'),(80,'B'),(89,'B'),(90,'A'),(100,'A')])
def test_grade_boundaries(score, grade):
    result = main.calculate_result(dict(korean=score, english=score, math=score))
    assert result == dict(total=score*3, average=score, grade=grade)


def test_crud_and_statistics(client):
    assert client.get('/').status_code == 200
    assert client.get('/students').json() == []
    empty = client.get('/subjects').json()
    assert len(empty) == 3
    assert all(row['student_count'] == 0 and row['total'] == 0 and row['average'] is None
               and row['minimum'] is None and row['maximum'] is None for row in empty)
    first = dict(name='홍길동', department='컴퓨터공학', korean=90, english=80, math=70)
    second = dict(name='김영희', department='경영학', korean=100, english=90, math=80)
    response = client.post('/students', json=first)
    assert response.status_code == 201
    one = response.json()
    two = client.post('/students', json=second).json()
    assert (one['total'], one['average'], one['grade']) == (240, 80, 'B')
    assert client.get(f"/students/{one['id']}").json() == one
    assert len(client.get('/students?q=컴퓨터').json()) == 1
    assert client.get("/students", params={'q':"' OR 1=1 --"}).json() == []
    stats = client.get('/subjects').json()
    assert stats[0] == dict(subject='korean',student_count=2,total=190,average=95,minimum=90,maximum=100)
    # 검색은 통계 범위를 좁히지 않습니다.
    assert len(client.get('/students?q=홍').json()) == 1
    assert client.get('/subjects').json() == stats
    first['math'] = 100
    for _ in range(2):  # 동일값 재수정도 성공
        updated = client.put(f"/students/{one['id']}",json=first)
        assert updated.status_code == 200
        assert updated.json()['grade'] == 'A'
    assert client.get('/subjects').json()[2]['average'] == 90
    assert client.delete(f"/students/{one['id']}").status_code == 204
    assert client.get('/subjects').json()[0]['student_count'] == 1
    assert client.get(f"/students/{one['id']}").status_code == 404
    assert client.put(f"/students/{one['id']}",json=first).status_code == 404
    assert client.delete(f"/students/{one['id']}").status_code == 404
    assert client.delete(f"/students/{two['id']}").status_code == 204
    assert client.get('/subjects').json() == empty


@pytest.mark.parametrize('score', [-1,101,0.5,'90',True])
def test_invalid_scores(client, score):
    response = client.post('/students',json=dict(name='학생',department='학과',korean=score))
    assert response.status_code == 422
    assert client.get('/students').json() == []


def test_empty_score_duplicate_score_and_validation(client):
    for _ in range(2):
        response = client.post('/students',json=dict(name=' 학생 ',department=' 학과 ',korean='',english=None))
        assert response.status_code == 201
        assert response.json()['total'] == 0 and response.json()['name'] == '학생'
    assert all(row['student_count'] == 2 and row['minimum'] == 0 for row in client.get('/subjects').json())
    assert client.post('/students',json=dict(name=' ',department='학과')).status_code == 422
    assert client.post('/students',json=dict(name='학생',department='학과',total=300)).status_code == 422
    calculated = client.post('/scores',json=[dict(name='학생',department='학과',korean=100,english=100,math=69)])
    assert calculated.json() == [dict(total=269,average=89.67,grade='B')]
    assert len(client.get('/students').json()) == 2  # 계산은 저장하지 않음


def test_db_error(client, monkeypatch):
    def failed_connection():
        raise main.pymysql.OperationalError(2003, 'test connection failure')
    monkeypatch.setattr(main, 'connect_db', failed_connection)
    response = client.get('/students')
    assert response.status_code == 503
    assert 'test connection failure' not in response.text
