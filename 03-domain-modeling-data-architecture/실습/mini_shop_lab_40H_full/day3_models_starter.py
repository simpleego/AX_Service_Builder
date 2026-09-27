
# Day 3 - models.py STARTER
# pip install sqlalchemy alembic pymysql faker
# SQLAlchemy 2.0 Declarative 스타일
from datetime import datetime
from typing import List, Optional
from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Index, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
import enum

class Base(DeclarativeBase):
    pass

# --- Enums ---
class OrderStatus(str, enum.Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    PREPARING = "PREPARING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"

class PaymentStatus(str, enum.Enum):
    READY = "READY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"

# --- TODO: 학생이 직접 완성 ---
class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # TODO: relationship 추가
    # cart: Mapped["Cart"] = relationship(back_populates="user")
    # orders: Mapped[List["Order"]] = relationship(back_populates="user")

class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("categories.id"), nullable=True)
    depth: Mapped[int] = mapped_column(Integer, default=0)

    # 자기참조
    parent: Mapped[Optional["Category"]] = relationship(back_populates="children", remote_side="Category.id")
    children: Mapped[List["Category"]] = relationship(back_populates="parent")

class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    # TODO: Day 3 오후에 추가
    # categories: Mapped[List["Category"]] = relationship(secondary="product_categories")

# 아래는 학생이 직접 만들어야 할 모델 힌트
# class Cart(Base): ...
# class CartItem(Base): ...
# class Order(Base): ...
# class OrderItem(Base): ...

# 실행 테스트
# from sqlalchemy import create_engine
# engine = create_engine("mysql+pymysql://root:1234@localhost/mini_shop", echo=True)
# Base.metadata.create_all(engine)
