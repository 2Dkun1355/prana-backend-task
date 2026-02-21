import uuid
from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from .database import Base

class User(AsyncAttrs, Base):
    """
    Database model representing a registered user.
    """
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    surname: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)