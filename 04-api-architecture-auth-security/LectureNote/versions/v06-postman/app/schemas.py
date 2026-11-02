from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator
Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
class TodoCreate(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: Title
    completed: bool = Field(default=False, strict=True)
class TodoPatch(BaseModel):
    model_config = ConfigDict(extra='forbid')
    title: Title | None = None
    completed: bool | None = Field(default=None, strict=True)
    @model_validator(mode='after')
    def check_patch(self):
        # PATCH는 전달한 필드만 바꾼다. 빈 객체/명시적 null은 허용하지 않는다.
        if not self.model_fields_set or any(getattr(self, k) is None for k in self.model_fields_set):
            raise ValueError('하나 이상의 title/completed 필드를 null 없이 입력하세요.')
        return self
class TodoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime
class TodoPage(BaseModel):
    data: list[TodoOut]
    page: int
    limit: int
