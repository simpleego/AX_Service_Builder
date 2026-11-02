"""기존 컬렉션을 유지하고 Idemcontents 전용 반복 요청 컬렉션을 추가한다."""
import copy
import json
from pathlib import Path
root = Path(__file__).resolve().parents[1]
source = json.loads((root/'postman/Todo-Course.postman_collection.json').read_text(encoding='utf-8'))
register = copy.deepcopy(source['item'][1]['item'][0])
register['name'] = '01 가입 및 환경 초기화'
register['event'][0]['script']['exec'].append("pm.environment.set('idemKey','todo-'+Date.now()+'-'+Math.random().toString(16).slice(2));")
login = copy.deepcopy(source['item'][1]['item'][3])
login['name'] = '02 로그인 및 토큰 저장'
def request(name, method, path, status, body=None, key=None, extra=''):
    headers = [{'key':'Authorization','value':'Bearer {{accessToken}}'}]
    value = {'method':method,'header':headers,'url':'{{baseUrl}}'+path}
    if key is not None: headers.append({'key':'Idempotency-Key','value':key})
    if body is not None:
        headers.append({'key':'Content-Type','value':'application/json'})
        value['body'] = {'mode':'raw','raw':json.dumps(body,ensure_ascii=False),'options':{'raw':{'language':'json'}}}
    code = f"pm.test('HTTP {status}',()=>pm.response.to.have.status({status}));\n"+extra
    return {'name':name,'request':value,'event':[{'listen':'test','script':{'type':'text/javascript','exec':code.splitlines()}}]}
title = {'title':'멱등성 실습','completed':False}
items = [register,login,
    request('03 키 있는 최초 생성','POST','/api/todos',201,title,'{{idemKey}}',
        "pm.environment.set('todoId',pm.response.json().id); pm.environment.set('idemOriginal',JSON.stringify(pm.response.json())); pm.environment.set('idemLocation',pm.response.headers.get('Location')); pm.test('최초 생성',()=>pm.expect(pm.response.headers.get('Idempotency-Replayed')).to.eql('false'));"),
    request('04 같은 키 재생','POST','/api/todos',201,title,'{{idemKey}}',
        "pm.test('원본 응답 재생',()=>{pm.expect(pm.response.json()).to.deep.eql(JSON.parse(pm.environment.get('idemOriginal'))); pm.expect(pm.response.headers.get('Location')).to.eql(pm.environment.get('idemLocation')); pm.expect(pm.response.headers.get('Idempotency-Replayed')).to.eql('true');});"),
    request('05 다른 본문 충돌','POST','/api/todos',409,{'title':'변경된 요청'},'{{idemKey}}'),
    request('06 GET 기준 저장','GET','/api/todos/{{todoId}}',200,extra="pm.environment.set('idemGet',JSON.stringify(pm.response.json()));"),
    request('07 GET 반복 불변','GET','/api/todos/{{todoId}}',200,extra="pm.test('조회 불변',()=>pm.expect(pm.response.json()).to.deep.eql(JSON.parse(pm.environment.get('idemGet'))));"),
    request('08 PATCH 첫 변경','PATCH','/api/todos/{{todoId}}',200,{'completed':True},extra="pm.environment.set('idemPatched',JSON.stringify(pm.response.json()));"),
    request('09 PATCH 반복 불변','PATCH','/api/todos/{{todoId}}',200,{'completed':True},extra="pm.test('updated_at 포함 동일',()=>pm.expect(pm.response.json()).to.deep.eql(JSON.parse(pm.environment.get('idemPatched'))));"),
    request('10 최초 삭제','DELETE','/api/todos/{{todoId}}',204),
    request('11 반복 삭제','DELETE','/api/todos/{{todoId}}',404),
    request('12 삭제 후에도 생성 응답만 재생','POST','/api/todos',201,title,'{{idemKey}}',
        "pm.test('최초 스냅샷',()=>pm.expect(pm.response.json()).to.deep.eql(JSON.parse(pm.environment.get('idemOriginal'))));"),
    request('13 재생으로 다시 생성되지 않음','GET','/api/todos/{{todoId}}',404),
    request('14 키 없는 POST 첫 생성','POST','/api/todos',201,title,extra="pm.environment.set('noKeyId1',pm.response.json().id);"),
    request('15 키 없는 POST 중복 생성','POST','/api/todos',201,title,extra="pm.environment.set('noKeyId2',pm.response.json().id); pm.test('다른 ID',()=>pm.expect(pm.response.json().id).not.to.eql(Number(pm.environment.get('noKeyId1'))));"),
    request('16 키 없는 Todo 정리 1','DELETE','/api/todos/{{noKeyId1}}',204),
    request('17 키 없는 Todo 정리 2','DELETE','/api/todos/{{noKeyId2}}',204),
    request('18 잘못된 키 형식','POST','/api/todos',400,title,'invalid key'),
]
collection = {'info':{'name':'Idemcontents · 멱등성 추가 실습','schema':source['info']['schema'],
    'description':'Idemcontents 서버와 Todo local 환경에서 전체를 순서대로 실행. 최초 응답 재생/충돌/GET/PATCH/DELETE 반복 검증.'},'item':items}
out = root/'postman/Idemcontents.postman_collection.json'
out.write_text(json.dumps(collection,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(f'{len(items)} Postman requests: {out}')
