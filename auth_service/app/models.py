from datetime import date
from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs
from app.database import Base

class User(AsyncAttrs, Base):
    """
    Database model representing a registered user.
    """
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(64), nullable=False)
    last_name: Mapped[str] = mapped_column(String(64), nullable=False)
    email: Mapped[str] = mapped_column(String(128), unique=True, index=True, nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    password: Mapped[str] = mapped_column(String(128), nullable=False)