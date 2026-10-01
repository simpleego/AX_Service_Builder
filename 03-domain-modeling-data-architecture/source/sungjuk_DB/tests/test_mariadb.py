"""전용 빈 MariaDB 테스트 DB에서만 실행하세요.

1. 관리자 계정으로 sungjuk_test DB를 생성하고 schema.sql의 테이블을 만드세요.
2. 테스트 계정에 sungjuk_test의 SELECT/INSERT/UPDATE/DELETE 권한을 부여하세요.
3. PowerShell 환경변수를 테스트 계정에 맞게 지정하세요.
   $env:DB_NAME='sungjuk_test'
   $env:DB_USER='테스트계정'
   $env:DB_PASSWORD='테스트비밀번호'
   $env:RUN_MARIADB_TESTS='1'
   python -m pytest -q tests/test_mariadb.py

기존 학생이 있는 DB에서는 실행을 거부합니다. 테스트가 생성한 학생만 정리합니다.
"""
import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import main

pytestmark = pytest.mark.skipif(os.getenv('RUN_MARIADB_TESTS') != '1', reason='실제 MariaDB 테스트는 명시적으로 활성화')


def test_real_mariadb_crud():
    assert os.getenv('DB_NAME', '').endswith('_test'), 'DB_NAME은 전용 _test DB여야 합니다.'
    ids = []
    with TestClient(main.app) as client:
        response = client.get('/students')
        assert response.status_code == 200, response.text
        assert response.json() == [], '빈 테스트 DB가 필요합니다.'
        try:
            for name, scores in [('홍길동',(90,80,70)),('김영희',(100,90,80))]:
                response = client.post('/students',json=dict(name=name,department='테스트',
                    korean=scores[0],english=scores[1],math=scores[2]))
                assert response.status_code == 201, response.text
                ids.append(response.json()['id'])
            assert client.get('/subjects').json()[0] == dict(subject='korean',student_count=2,total=190,average=95,minimum=90,maximum=100)
            assert len(client.get('/students?q=홍').json()) == 1
            payload = dict(name='홍길동',department='테스트',korean=90,english=80,math=100)
            for _ in range(2):
                response = client.put(f'/students/{ids[0]}',json=payload)
                assert response.status_code == 200, response.text
                assert response.json()['grade'] == 'A'
            assert client.get('/subjects').json()[2]['average'] == 90
            for student_id in ids:
                assert client.delete(f'/students/{student_id}').status_code == 204
                assert client.get(f'/students/{student_id}').status_code == 404
            assert all(stat['student_count'] == 0 and stat['average'] is None for stat in client.get('/subjects').json())
        finally:
            for student_id in ids:
                client.delete(f'/students/{student_id}')
