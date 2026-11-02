"""POST 생성의 선택적 멱등성. 키 범위는 인증 사용자 + 작업 + 키이며 DB에 영구 보관한다."""
import hashlib
import json
import re
from fastapi import HTTPException
from sqlalchemy import select
from .models import User, IdempotencyRecord
from .schemas import TodoOut
from .todo_repository import TodoRepository

OPERATION = 'POST:/api/todos'

def create_idempotent(db, owner, data, key):
    if not re.fullmatch(r'[A-Za-z0-9._:-]{1,128}', key):
        raise HTTPException(400, 'INVALID_IDEMPOTENCY_KEY')
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    # 검증/정규화된 DTO로 계산한다. JSON 순서, 앞뒤 공백, 생략된 기본값 차이는 같은 요청이다.
    canonical = json.dumps(data.model_dump(), sort_keys=True, ensure_ascii=False, separators=(',', ':'))
    request_hash = hashlib.sha256(canonical.encode()).hexdigest()

    # 먼저 사용자 행을 잠근다. 첫 요청에 아직 키 row가 없어도 동시 요청을 직렬화할 수 있다.
    # 메모리 락과 달리 여러 worker/서버에서도 MySQL의 동일 행 잠금이 적용된다.
    user_id = db.scalar(select(User.id).where(User.id == owner).with_for_update())
    if user_id is None:
        raise HTTPException(401, 'UNAUTHORIZED')
    # FOR UPDATE는 MySQL REPEATABLE READ에서도 선행 요청이 커밋한 최신 기록을 읽는다.
    record = db.scalar(select(IdempotencyRecord).where(
        IdempotencyRecord.user_id == owner, IdempotencyRecord.operation == OPERATION,
        IdempotencyRecord.key_hash == key_hash).with_for_update())
    if record is not None:
        if record.request_hash != request_hash:
            raise HTTPException(409, 'IDEMPOTENCY_KEY_CONFLICT')
        body, status, location = json.loads(record.response_body), record.status_code, record.location
        db.commit()  # 읽기 재생에서도 잠금을 즉시 해제한다.
        return body, status, location, True

    todo = TodoRepository(db).add(owner, data.model_dump())
    db.flush()  # ID와 DB 기본 timestamp를 얻되 아직 커밋하지 않는다.
    db.refresh(todo)
    body = TodoOut.model_validate(todo).model_dump(mode='json')
    location = f'/api/todos/{todo.id}'
    db.add(IdempotencyRecord(user_id=owner, operation=OPERATION, key_hash=key_hash,
        request_hash=request_hash, response_body=json.dumps(body, ensure_ascii=False),
        status_code=201, location=location))
    # Todo와 응답 기록을 원자적으로 커밋한다. 기록 저장 실패 시 Todo도 get_db에서 롤백된다.
    db.commit()
    return body, 201, location, False
