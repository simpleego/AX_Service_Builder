from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from app.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=True)  # 소셜 로그인 전용 계정은 비어있을 수 있음
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    todos = relationship("Todo", back_populates="owner", cascade="all, delete-orphan")
    refresh_sessions = relationship(
        "RefreshSession", back_populates="user", cascade="all, delete-orphan"
    )
