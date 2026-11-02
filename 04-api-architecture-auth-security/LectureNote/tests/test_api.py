"""라우터를 통해 CRUD 계약/검증/소유권을 검증한다. 구현 내부 값을 단순 복제하지 않는다."""
import pytest
from conftest import AUTH, VERSION, STAGE, signup

def test_health_and_contract(client):
    assert client.get('/health').json() == {'status':'ok'}
    schema = client.get('/openapi.json')
    assert schema.status_code == (404 if VERSION.startswith('v01') else 200)
    assert client.get('/docs').status_code == (200 if STAGE >= 5 else 404)
    if schema.status_code == 200:
        assert 'post' in schema.json()['paths']['/api/todos']
        assert schema.json()['components']['schemas']['TodoCreate']['properties']['title']['maxLength'] == 200

def test_crud_contract(client, headers):
    result = client.post('/api/todos', headers=headers, json={'title':'  첫 실습  '})
    assert result.status_code == 201
    todo = result.json()
    assert todo['title'] == '첫 실습' and todo['completed'] is False
    path = '/api/todos/'+str(todo['id'])
    assert result.headers['location'] == path
    assert client.get(path, headers=headers).status_code == 200
    page = client.get('/api/todos?completed=false&page=1&limit=1', headers=headers).json()
    assert page['data'][0]['id'] == todo['id'] and page['page'] == 1
    patched = client.patch(path, headers=headers, json={'completed':True})
    assert patched.status_code == 200 and patched.json()['completed'] is True
    assert client.get('/api/todos?completed=false', headers=headers).json()['data'] == []
    deleted = client.delete(path, headers=headers)
    assert deleted.status_code == 204 and deleted.content == b''
    assert client.get(path, headers=headers).status_code == 404
    assert client.delete(path, headers=headers).status_code == 404

@pytest.mark.parametrize('body',[{'title':''},{'title':' '},{'title':'a'*201},{'title':'test','owner_id':2},
    {'title':'test','completed':'true'}, {'title':None}, []])
def test_create_validation(client, headers, body):
    response = client.post('/api/todos', headers=headers, json=body)
    assert response.status_code == 422
    assert response.json()['error']['code'] == 'VALIDATION_ERROR'

@pytest.mark.parametrize('body',[{}, {'title':None}, {'completed':None}, {'completed':'true'}, {'other':1}])
def test_patch_validation(client, headers, body):
    assert client.patch('/api/todos/1', headers=headers, json=body).status_code == 422

@pytest.mark.parametrize('query',['page=0','limit=101','page=abc','completed=bad'])
def test_pagination_validation(client, headers, query):
    assert client.get('/api/todos?'+query, headers=headers).status_code == 422

@pytest.mark.skipif(not AUTH, reason='v03 이상 인증 실습')
def test_owner_isolation(client, tokens, headers):
    todo = client.post('/api/todos', headers=headers, json={'title':'A의 개인 정보'}).json()
    other, _ = signup(client, 'other@example.com')
    b = {'Authorization':'Bearer '+other['accessToken']}
    path = '/api/todos/'+str(todo['id'])
    assert client.get('/api/todos').status_code == 401
    assert client.get('/api/todos', headers=b).json()['data'] == []
    assert client.get(path, headers=b).status_code == 404
    assert client.patch(path, headers=b, json={'title':'공격'}).status_code == 404
    assert client.delete(path, headers=b).status_code == 404
    assert client.get(path, headers=headers).json()['title'] == 'A의 개인 정보'
