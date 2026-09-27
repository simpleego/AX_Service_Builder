
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ProductResponse(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    review_avg: float = 0
    review_count: int = 0
    is_active: bool
    class Config: from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(default=1, ge=1)

class CartResponse(BaseModel):
    id: int
    user_id: int
    items: List[ProductResponse] = []
    total_amount: int = 0
    class Config: from_attributes = True

class OrderCreate(BaseModel):
    user_id: int
    coupon_code: Optional[str] = None

class OrderItemResponse(BaseModel):
    product_name: str
    unit_price: int
    quantity: int
    subtotal: int
    class Config: from_attributes = True

class OrderResponse(BaseModel):
    id: int
    order_no: str
    status: str
    total_amount: int
    final_amount: int
    created_at: datetime
    items: List[OrderItemResponse] = []
    class Config: from_attributes = True
