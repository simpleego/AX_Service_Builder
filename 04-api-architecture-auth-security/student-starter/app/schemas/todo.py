from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

from app.schemas.tag import TagOut


class TodoCreate(BaseModel):
    title: str
    content: Optional[str] = None
    due_date: Optional[datetime] = None
    tag_names: list[str] = []  # 6일차: 생성 시 태그를 함께 지정


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None
    tag_names: Optional[list[str]] = None


class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    title: str
    content: Optional[str]
    status: str
    due_date: Optional[datetime]
    created_at: datetime
    tags: list[TagOut] = []
