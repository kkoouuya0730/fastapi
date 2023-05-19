import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import TIMESTAMP, Boolean, Column, DateTime, Integer, String, text
from sqlalchemy.dialects.postgresql import UUID

from ..database import Base

JST = timezone(timedelta(hours=+9), "JST")


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    username = Column(String, nullable=False, default="user")
    email = Column(String, nullable=False)
    full_name = Column(String, nullable=False, default="")
    password = Column(String, nullable=False)
    # created_at = Column(DateTime(timezone=JST), server_default=datetime.now(JST), nullable=False)
    # updated_at = Column(DateTime(timezone=JST), server_default=datetime.now(JST), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
    updated_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )
