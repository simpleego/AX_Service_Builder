"""반복 요청의 응답뿐 아니라 DB 행 수, 쓰기 SQL, 롤백 결과를 검증한다."""
import pytest
from sqlalchemy import select, func, event
from conftest import VERSION, models, signup
pytestmark = pytest.mark.skipif(VERSION != 'Idemcontents', reason='Idemcontents 추가 실습')

def keyed(headers, value='lesson-key-001'):
    return {**headers, 'Idempotency-Key':value}

def test_post_replays_snapshot_and_rejects_changed_body(context, headers):
    client, factory = context
    first = client.post('/api/todos', headers=keyed(headers), json={'title':'  같은 요청  '})
    second = client.post('/api/todos', headers=keyed(headers), json={'completed':False,'title':'같은 요청'})
    assert first.status_code == second.status_code == 201
    assert first.json() == second.json()
    assert first.headers['location'] == second.headers['location']
    assert first.headers['idempotency-replayed'] == 'false'
    assert second.headers['idempotency-replayed'] == 'true'
    assert client.post('/api/todos', headers=keyed(headers), json={'title':'다른 요청'}).status_code == 409
    with factory() as db:
        assert db.scalar(select(func.count()).select_from(models.Todo)) == 1
        assert db.scalar(select(func.count()).select_from(models.IdempotencyRecord)) == 1
    # 최초 응답 스냅샷은 현재 Todo 표현이 아니다. 삭제 후 재시도해도 재생만 하고 다시 만들지 않는다.
    client.delete(first.headers['location'], headers=headers)
    third = client.post('/api/todos', headers=keyed(headers), json={'title':'같은 요청'})
    assert third.json() == first.json()
    assert client.get(first.headers['location'], headers=headers).status_code == 404

def test_key_scope_user_and_optional_key(client, headers):
    a = client.post('/api/todos', headers=keyed(headers), json={'title':'공통 제목'})
    other, _ = signup(client, 'idem-other@example.com')
    b_headers = keyed({'Authorization':'Bearer '+other['accessToken']})
    b = client.post('/api/todos', headers=b_headers, json={'title':'공통 제목'})
    assert a.status_code == b.status_code == 201 and a.json()['id'] != b.json()['id']
    c = client.post('/api/todos', headers=keyed(headers,'different-key'), json={'title':'공통 제목'})
    assert c.status_code == 201 and c.json()['id'] != a.json()['id']
    normal = [client.post('/api/todos', headers=headers, json={'title':'키 없는 POST'}).json()['id'] for _ in range(2)]
    assert normal[0] != normal[1]
    assert client.post('/api/todos', headers={'Idempotency-Key':'public-key'}, json={'title':'비인증'}).status_code == 401

@pytest.mark.parametrize('key',['', 'contains space', 'a'*129, 'bad/key'])
def test_invalid_key(client, headers, key):
    assert client.post('/api/todos', headers=keyed(headers,key), json={'title':'제목'}).status_code == 400

def test_invalid_body_does_not_reserve_key(client, headers):
    assert client.post('/api/todos', headers=keyed(headers), json={'title':''}).status_code == 422
    response = client.post('/api/todos', headers=keyed(headers), json={'title':'정상'})
    assert response.status_code == 201 and response.headers['idempotency-replayed']=='false'

def test_record_failure_rolls_back_todo_and_allows_retry(context, headers):
    client, factory = context
    def fail_insert(*_args):
        raise RuntimeError('simulated persistence failure')
    event.listen(models.IdempotencyRecord, 'before_insert', fail_insert)
    try:
        with pytest.raises(RuntimeError, match='simulated persistence failure'):
            client.post('/api/todos', headers=keyed(headers), json={'title':'원자성 실습'})
    finally:
        event.remove(models.IdempotencyRecord, 'before_insert', fail_insert)
    with factory() as db:
        assert db.scalar(select(func.count()).select_from(models.Todo)) == 0
        assert db.scalar(select(func.count()).select_from(models.IdempotencyRecord)) == 0
    assert client.post('/api/todos', headers=keyed(headers), json={'title':'원자성 실습'}).status_code == 201

def test_get_patch_delete_repetition_without_writes(context, headers):
    client, factory = context
    created = client.post('/api/todos', headers=headers, json={'title':'반복 동작'})
    path = created.headers['location']
    first_patch = client.patch(path, headers=headers, json={'completed':True})
    assert first_patch.status_code == 200
    # 단순 timestamp 비교만으로는 초 단위 정밀도 때문에 잘못 통과할 수 있다. 실제 쓰기 SQL도 잡는다.
    writes = []
    def capture(_conn, _cursor, statement, _parameters, _context, _many):
        if statement.lstrip().upper().startswith(('INSERT ', 'UPDATE ', 'DELETE ')):
            writes.append(statement)
    engine = factory.kw['bind']
    event.listen(engine, 'before_cursor_execute', capture)
    try:
        get_results = [client.get(path, headers=headers).json() for _ in range(2)]
        patches = [client.patch(path, headers=headers, json={'completed':True}).json() for _ in range(2)]
        assert get_results[0] == get_results[1] == first_patch.json()
        assert all(result == first_patch.json() for result in patches)
        assert writes == []
    finally:
        event.remove(engine, 'before_cursor_execute', capture)
    assert client.delete(path, headers=headers).status_code == 204
    assert client.delete(path, headers=headers).status_code == 404
    with factory() as db:
        assert db.scalar(select(func.count()).select_from(models.Todo)) == 0
