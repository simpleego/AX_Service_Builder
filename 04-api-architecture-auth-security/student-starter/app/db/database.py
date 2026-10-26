"""
2일차: 계층형 아키텍처의 기반 — DB 세션을 DI로 공급
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """요청 단위로 세션을 열고, 끝나면 반드시 닫는다 (FastAPI Depends용)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
