import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

JST = timezone(timedelta(hours=+9), "JST")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    title = Column(String)
    description = Column(String)
    is_done = Column(Boolean, server_default="False")
    # created_at = Column(DateTime(timezone=JST), server_default=datetime.now(JST), nullable=False)
    # updated_at = Column(DateTime(timezone=JST), server_default=datetime.now(JST), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
