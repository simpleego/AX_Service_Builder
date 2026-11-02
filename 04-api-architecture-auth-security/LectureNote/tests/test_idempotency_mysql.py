"""선택: 마이그레이션 완료된 별도 MySQL 실습 DB에서 실제 동시성 검증. SQLite로 대체하지 않는다."""
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import pytest
from sqlalchemy import create_engine, select, func, delete
from sqlalchemy.orm import sessionmaker
from conftest import VERSION

@pytest.mark.skipif(VERSION != 'Idemcontents' or not os.getenv('IDEMPOTENCY_MYSQL_TEST_URL'),
                    reason='Idemcontents + 별도 MySQL 테스트 URL 설정 필요')
def test_mysql_concurrent_same_key():
    from app.models import User, Todo, IdempotencyRecord
    from app.schemas import TodoCreate
    from app.idempotency import create_idempotent
    engine = create_engine(os.environ['IDEMPOTENCY_MYSQL_TEST_URL'], pool_pre_ping=True)
    assert engine.dialect.name == 'mysql', 'MySQL 테스트 URL을 사용하세요.'
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as db:
        user = User(email=f'idem-{uuid.uuid4().hex}@example.com', password_hash=None)
        db.add(user)
        db.commit()
        owner = user.id
    barrier = Barrier(4)
    def send():
        with factory() as db:
            try:
                barrier.wait(timeout=15)
                return create_idempotent(db, owner, TodoCreate(title='동시 생성'), 'concurrent-key')
            except Exception:
                db.rollback()
                raise
    try:
        with ThreadPoolExecutor(max_workers=4) as workers:
            results = list(workers.map(lambda _: send(), range(4)))
        assert len({r[0]['id'] for r in results}) == 1
        assert sum(not r[3] for r in results) == 1
        assert all(r[1]==201 for r in results)
        with factory() as db:
            assert db.scalar(select(func.count()).select_from(Todo).where(Todo.owner_id==owner)) == 1
            assert db.scalar(select(func.count()).select_from(IdempotencyRecord).where(IdempotencyRecord.user_id==owner)) == 1
    finally:
        # 이 테스트에서 생성한 사용자와 종속 행만 정리한다. 스키마/기존 사용자 데이터는 건드리지 않는다.
        with factory() as db:
            db.execute(delete(IdempotencyRecord).where(IdempotencyRecord.user_id==owner))
            db.execute(delete(Todo).where(Todo.owner_id==owner))
            db.execute(delete(User).where(User.id==owner))
            db.commit()
        engine.dispose()
