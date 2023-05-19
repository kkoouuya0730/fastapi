from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator

from .common import DateTimeModelMixin, IdModelMixin

JST = timezone(timedelta(hours=+9), "JST")


class TodoBase(BaseModel):
    title: str

    # titleは半角英数字のみ
    # バリデーションエラーを出すことはできるけど500エラーになる
    @validator("title")
    def title_must_hulf_width(cls, v: str):
        if not cls.__isalnum_ascii(v):
            raise ValueError("title must hulf width")
        return v.title()

    def __isalnum_ascii(s: str):
        return True if s.isalnum() and s.isascii() else False


class TodoCreate(TodoBase):
    description: Optional[str] = Field(None, min_length=0, max_length=50)


class Todo(TodoCreate, DateTimeModelMixin, IdModelMixin):
    is_done: bool = Field(default=False)

    class Config:
        orm_mode = True
