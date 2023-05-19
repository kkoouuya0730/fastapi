from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, constr, validator

from .common import DateTimeModelMixin, IdModelMixin


class UserCreate(BaseModel):
    username: str = Field("user", min_length=1, max_length=50)
    email: EmailStr
    password: constr(min_length=8, max_length=100)


class UserOut(BaseModel):
    user_id: UUID
    username: str
    access_token: str


class User(DateTimeModelMixin, IdModelMixin):
    username: str = Field("user", min_length=1, max_length=50)
    email: Optional[str] = ""
    full_name: Optional[str] = ""
    password: str

    class Config:
        orm_mode = True
