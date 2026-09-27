
# Day 3 - models.py COMPLETE (교강사용 정답)
from datetime import datetime
from typing import List, Optional
import enum
from sqlalchemy import BigInteger, String, Integer, Boolean, DateTime, ForeignKey, UniqueConstraint, Index, Text, SmallInteger, DECIMAL
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Enum as SAEnum

class Base(DeclarativeBase): pass

class OrderStatus(str, enum.Enum):
    PENDING="PENDING"; PAID="PAID"; PREPARING="PREPARING"; SHIPPED="SHIPPED"; DELIVERED="DELIVERED"; CANCELLED="CANCELLED"
class PaymentMethod(str, enum.Enum):
    CARD="CARD"; TRANSFER="TRANSFER"; KAKAO_PAY="KAKAO_PAY"
class PaymentStatus(str, enum.Enum):
    READY="READY"; COMPLETED="COMPLETED"; FAILED="FAILED"; CANCELLED="CANCELLED"
class DiscountType(str, enum.Enum):
    RATE="RATE"; FIXED="FIXED"

class User(Base):
    __tablename__="users"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    email: Mapped[str]=mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str]=mapped_column(String(255))
    name: Mapped[str]=mapped_column(String(100))
    phone: Mapped[Optional[str]]=mapped_column(String(20))
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.now)
    cart: Mapped[Optional["Cart"]]=relationship(back_populates="user", cascade="all, delete-orphan", uselist=False)
    orders: Mapped[List["Order"]]=relationship(back_populates="user")

class Category(Base):
    __tablename__="categories"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]=mapped_column(String(100))
    parent_id: Mapped[Optional[int]]=mapped_column(ForeignKey("categories.id"))
    depth: Mapped[int]=mapped_column(default=0)
    parent: Mapped[Optional["Category"]]=relationship(back_populates="children", remote_side="Category.id")
    children: Mapped[List["Category"]]=relationship(back_populates="parent")

class Product(Base):
    __tablename__="products"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]=mapped_column(String(200))
    slug: Mapped[Optional[str]]=mapped_column(String(200), unique=True)
    price: Mapped[int]=mapped_column(Integer)
    compare_price: Mapped[Optional[int]]=mapped_column(Integer)
    stock: Mapped[int]=mapped_column(default=0)
    review_count: Mapped[int]=mapped_column(default=0)
    review_avg: Mapped[float]=mapped_column(DECIMAL(3,2), default=0)
    is_active: Mapped[bool]=mapped_column(Boolean, default=True)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.now)
    cart_items: Mapped[List["CartItem"]]=relationship(back_populates="product")
    order_items: Mapped[List["OrderItem"]]=relationship(back_populates="product")

class ProductCategory(Base):
    __tablename__="product_categories"
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"), primary_key=True)
    category_id: Mapped[int]=mapped_column(ForeignKey("categories.id"), primary_key=True)

class Cart(Base):
    __tablename__="carts"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"]=relationship(back_populates="cart")
    items: Mapped[List["CartItem"]]=relationship(back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__="cart_items"
    __table_args__=(UniqueConstraint("cart_id","product_id", name="uq_cart_product"),)
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    cart_id: Mapped[int]=mapped_column(ForeignKey("carts.id"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int]=mapped_column(default=1)
    cart: Mapped["Cart"]=relationship(back_populates="items")
    product: Mapped["Product"]=relationship(back_populates="cart_items")

class Order(Base):
    __tablename__="orders"
    __table_args__=(Index("idx_orders_user_created","user_id","created_at"),)
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_no: Mapped[str]=mapped_column(String(20), unique=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.id"))
    status: Mapped[OrderStatus]=mapped_column(SAEnum(OrderStatus), default=OrderStatus.PENDING)
    total_amount: Mapped[int]=mapped_column(Integer)
    discount_amount: Mapped[int]=mapped_column(default=0)
    final_amount: Mapped[int]=mapped_column(Integer)
    created_at: Mapped[datetime]=mapped_column(DateTime, default=datetime.now)
    user: Mapped["User"]=relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]]=relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__="order_items"
    id: Mapped[int]=mapped_column(BigInteger, primary_key=True, autoincrement=True)
    order_id: Mapped[int]=mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int]=mapped_column(ForeignKey("products.id"))
    product_name: Mapped[str]=mapped_column(String(200))
    unit_price: Mapped[int]=mapped_column(Integer)
    quantity: Mapped[int]=mapped_column(Integer)
    subtotal: Mapped[int]=mapped_column(Integer)
    order: Mapped["Order"]=relationship(back_populates="items")
    product: Mapped["Product"]=relationship(back_populates="order_items")
