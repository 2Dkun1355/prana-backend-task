from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine
)
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    url=settings.async_database_url,
    echo=False,
    future=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)

async_session_local = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession
)

class Base(DeclarativeBase):
    """
    Base class for declarative class definitions.
    """
    pass


async def init_db() -> None:
    """
    Initializes the database by creating all tables defined in the metadata.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_db() -> None:
    """
    Drops all tables defined in the metadata.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provides an asynchronous database session for dependency injection.
    """
    async with async_session_local() as session:
        yield session