"""실제 import 가능한 Postman v2.1 컬렉션/환경을 생성한다."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
def script(lines):
    return {'type': 'text/javascript', 'exec': lines.splitlines()}
def req(name, method, path, status, body=None, token=None, after='', before=''):
    headers = []
    if token:
        headers.append({'key': 'Authorization', 'value': 'Bearer {{'+token+'}}'})
    request = {'method': method, 'header': headers, 'url': '{{baseUrl}}'+path,
        'description': '상태코드를 확인하고 필요한 응답값을 환경변수로 저장합니다. 순서대로 실행하세요.'}
    if body is not None:
        headers.append({'key': 'Content-Type', 'value': 'application/json'})
        request['body'] = {'mode': 'raw', 'raw': json.dumps(body, ensure_ascii=False), 'options': {'raw': {'language': 'json'}}}
    tests = f"pm.test('HTTP {status}', () => pm.response.to.have.status({status}));\n"+after
    if status == 204:
        tests += "\npm.test('빈 본문', () => pm.expect(pm.response.text()).to.eql(''));"
    events = [{'listen': 'test', 'script': script(tests)}]
    if before: events.insert(0, {'listen': 'prerequest', 'script': script(before)})
    return {'name': name, 'request': request, 'event': events, 'response': []}
save_todo = "if (pm.response.code===201) { pm.environment.set('todoId',pm.response.json().id); }"
todo_check = "pm.test('제목/완료 타입',()=>{ const x=pm.response.json(); pm.expect(x.title).to.be.a('string'); pm.expect(x.completed).to.be.a('boolean'); });"
public = [
    req('01 DB health','GET','/health',200),
    req('02 생성','POST','/api/todos',201,{'title':'REST 실습','completed':False},after=save_todo+'\n'+todo_check),
    req('03 목록','GET','/api/todos?page=1&limit=20',200,after="pm.test('배열',()=>pm.expect(pm.response.json().data).to.be.an('array'));"),
    req('04 상세','GET','/api/todos/{{todoId}}',200,after=todo_check),
    req('05 완료 수정','PATCH','/api/todos/{{todoId}}',200,{'completed':True},after="pm.test('완료',()=>pm.expect(pm.response.json().completed).to.eql(true));"),
    req('06 잘못된 제목','POST','/api/todos',422,{'title':' '}),
    req('07 owner 주입 차단','POST','/api/todos',422,{'title':'주입','owner_id':2}),
    req('08 빈 PATCH','PATCH','/api/todos/{{todoId}}',422,{}),
    req('09 삭제','DELETE','/api/todos/{{todoId}}',204),
    req('10 삭제 후 상세','GET','/api/todos/{{todoId}}',404),
]
def save_tokens(access='accessToken', refresh='refreshToken'):
    return f"if(pm.response.code===200){{ const t=pm.response.json(); pm.environment.set('{access}',t.accessToken); pm.environment.set('{refresh}',t.refreshToken); }}"
credentials_a = {'email':'{{emailA}}','password':'{{password}}'}
credentials_b = {'email':'{{emailB}}','password':'{{password}}'}
initialize = """// 반복 실행 시 중복 이메일을 피한다. secret 대신 공개된 실습용 비밀번호만 사용한다.
const run=Date.now()+'-'+Math.random().toString(16).slice(2);
pm.environment.set('emailA','student-a-'+run+'@example.com');
pm.environment.set('emailB','student-b-'+run+'@example.com');
for (const key of ['accessToken','refreshToken','accessTokenB','refreshTokenB','oldRefreshToken','todoId']) pm.environment.unset(key);"""
auth = [
    req('01 A 가입 / 시나리오 초기화','POST','/api/auth/register',201,credentials_a,before=initialize),
    req('02 중복 가입','POST','/api/auth/register',409,credentials_a),
    req('03 잘못된 비밀번호','POST','/api/auth/login',401,{'email':'{{emailA}}','password':'wrong-password-123'}),
    req('04 A 로그인 / 토큰 저장','POST','/api/auth/login',200,credentials_a,after=save_tokens()),
    req('05 A Todo 생성','POST','/api/todos',201,{'title':'A 전용 Todo'},'accessToken',save_todo+'\n'+todo_check),
    req('06 인증 없이 접근','GET','/api/todos',401),
    req('07 A 목록 필터','GET','/api/todos?completed=false&limit=10',200,token='accessToken',after="pm.test('내 Todo 포함',()=>pm.expect(pm.response.json().data.map(x=>x.id)).to.include(Number(pm.environment.get('todoId'))));"),
    req('08 B 가입','POST','/api/auth/register',201,credentials_b),
    req('09 B 로그인','POST','/api/auth/login',200,credentials_b,after=save_tokens('accessTokenB','refreshTokenB')),
    req('10 B로 A 상세 차단','GET','/api/todos/{{todoId}}',404,token='accessTokenB'),
    req('11 B로 A 수정 차단','PATCH','/api/todos/{{todoId}}',404,{'title':'타인 변경'},'accessTokenB'),
    req('12 B로 A 삭제 차단','DELETE','/api/todos/{{todoId}}',404,token='accessTokenB'),
    req('13 A 완료 수정','PATCH','/api/todos/{{todoId}}',200,{'completed':True},'accessToken'),
    req('14 빈 제목 차단','POST','/api/todos',422,{'title':''},'accessToken'),
    req('15 completed 타입 차단','PATCH','/api/todos/{{todoId}}',422,{'completed':'true'},'accessToken'),
    req('16 page 범위 차단','GET','/api/todos?page=0',422,token='accessToken'),
    req('17 A refresh 회전','POST','/api/auth/refresh',200,{'refreshToken':'{{refreshToken}}'},after=save_tokens(),before="// 회전 전 값을 보관해 재사용 공격을 재현한다.\npm.environment.set('oldRefreshToken',pm.environment.get('refreshToken'));"),
    req('18 이전 refresh 재사용 차단','POST','/api/auth/refresh',401,{'refreshToken':'{{oldRefreshToken}}'}),
    req('19 새 refresh도 family 폐기 확인','POST','/api/auth/refresh',401,{'refreshToken':'{{refreshToken}}'}),
    req('20 A 재로그인','POST','/api/auth/login',200,credentials_a,after=save_tokens()),
    req('21 A 삭제','DELETE','/api/todos/{{todoId}}',204,token='accessToken'),
    req('22 삭제 후 확인','GET','/api/todos/{{todoId}}',404,token='accessToken'),
    req('23 로그아웃','POST','/api/auth/logout',204,{'refreshToken':'{{refreshToken}}'}),
    req('24 로그아웃 후 refresh 차단','POST','/api/auth/refresh',401,{'refreshToken':'{{refreshToken}}'}),
    req('25 access는 만료 전까지 유효','GET','/api/todos',200,token='accessToken'),
]
google = [req('01 소셜 사용자 Todo 생성','POST','/api/todos',201,{'title':'Google 로그인 실습'},'accessToken',save_todo),
    req('02 소셜 사용자 목록','GET','/api/todos',200,token='accessToken'),
    req('03 잘못된 state 차단 (Google 설정 필요)','GET','/api/auth/google/callback?state=wrong&code=wrong',400),
    req('04 소셜 Todo 삭제','DELETE','/api/todos/{{todoId}}',204,token='accessToken')]
collection = {'info': {'name':'Todo API · 4과목 단계별 실습','schema':'https://schema.getpostman.com/json/collection/v2.1.0/collection.json',
    'description':'v01~v02: 01 폴더. v03 이상: 02 폴더. Google 브라우저 로그인 뒤 03 폴더. 전체 컬렉션을 한 번에 실행하지 마세요.'},
    'item':[{'name':'01 Public CRUD (v01-v02 only)','item':public},
            {'name':'02 Authenticated scenario (v03-v06)','item':auth},
            {'name':'03 Google manual follow-up (v04-v06)','item':google}]}
env = {'name':'Todo local', 'values':[{'key':k,'value':v,'enabled':True,'type':'secret' if 'Token' in k or k=='password' else 'default'} for k,v in {
    'baseUrl':'http://localhost:8000','password':'Classroom-Only-12345!','emailA':'','emailB':'','todoId':'',
    'accessToken':'','refreshToken':'','accessTokenB':'','refreshTokenB':'','oldRefreshToken':''}.items()], '_postman_variable_scope':'environment'}
out = ROOT/'postman'
out.mkdir(exist_ok=True)
for filename, obj in [('Todo-Course.postman_collection.json',collection),('local.postman_environment.json',env)]:
    (out/filename).write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
print('Generated Postman collection: 39 requests, 3 scenario folders.')
