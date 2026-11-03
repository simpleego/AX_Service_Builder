"""
DB 연결 모듈 (SQLAlchemy 2.x + PyMySQL)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import DATABASE_URL

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,   # 끊어진 커넥션 자동 감지 (MySQL wait_timeout 대비)
    echo=False,           # True로 바꾸면 실행되는 SQL이 콘솔에 출력됨 (수업 시 유용)
)

# 주의: 여기서 말하는 'Session'은 DB 작업 단위(트랜잭션)이며,
#       로그인 '세션 인증'의 세션과는 전혀 다른 개념입니다.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    """요청마다 DB 세션을 열고, 응답 후 닫는 FastAPI 의존성"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
