from datetime import datetime, timedelta, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, validator
from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, text

JST = timezone(timedelta(hours=+9), "JST")


class CoreModel(BaseModel):
    pass


class DateTimeModelMixin(BaseModel):
    created_at: datetime = Field(default_factory=datetime.now(JST))
    updated_at: datetime = Field(default_factory=datetime.now(JST))

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, v: datetime) -> datetime:
        return v or datetime.now(JST)

    @validator("updated_at")
    def updated_at_must_after_created_at(cls, v: datetime, values):
        if v < values["created_at"]:
            raise ValueError("updated_at must after created_at")
        return v


class IdModelMixin(BaseModel):
    id: UUID = Field(default_factory=uuid4)
