from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User


class UserRepository:
    """
    Repository for handling database operations related to the User model.
    """
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, **kwargs) -> User:
        """
        Creates a new user record in the database.
        """
        obj = User(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_email(self, email: str) -> User | None:
        """
        Retrieves a user from the database by their email address.
        """
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalars().first()