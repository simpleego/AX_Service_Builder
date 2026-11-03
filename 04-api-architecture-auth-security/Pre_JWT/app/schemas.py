"""
요청/응답 스키마 (Pydantic)
"""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignupRequest(BaseModel):
    username: str = Field(min_length=3, max_length=50, examples=["hong"])
    email: EmailStr = Field(examples=["hong@example.com"])
    password: str = Field(min_length=4, max_length=72, examples=["1234"])  # bcrypt는 72바이트까지 사용


class LoginRequest(BaseModel):
    username: str = Field(examples=["hong"])
    password: str = Field(examples=["1234"])


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ORM 객체 -> 응답 변환 허용

    id: int
    username: str
    email: str
    created_at: datetime | None = None


class MessageResponse(BaseModel):
    message: str


class SessionInfo(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: str      # 실습용으로 앞부분만 잘라서 보여줍니다
    created_at: datetime
    expires_at: datetime
    last_accessed_at: datetime
    ip_address: str | None
    user_agent: str | None
    is_current: bool = False
