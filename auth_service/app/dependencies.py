from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .core.security import PasswordManager, JWTManager
from .repository import UserRepository
from .services import AuthService

SessionDepends = Annotated[AsyncSession, Depends(get_session)]


def get_repository(session: SessionDepends) -> UserRepository:
    """
    Returns a UserRepository instance with an injected database session.
    """
    return UserRepository(session)


def get_password_manager() -> PasswordManager:
    """
    Returns a PasswordManager instance for hashing and password validation.
    """
    return PasswordManager()


def get_jwt_manager() -> JWTManager:
    """
    Returns a JWTManager instance for token operations.
    """
    return JWTManager()


RepositoryDepends = Annotated[UserRepository, Depends(get_repository)]
PasswordManagerDepends = Annotated[PasswordManager, Depends(get_password_manager)]
JWTManagerDepends = Annotated[JWTManager, Depends(get_jwt_manager)]


def get_auth_service(
    repository: RepositoryDepends,
    password_manager: PasswordManagerDepends,
    jwt_manager: JWTManagerDepends
) -> AuthService:
    """
    Returns an AuthService instance with injected repository and security managers.
    """
    return AuthService(
        repository=repository,
        password_manager=password_manager,
        jwt_manager=jwt_manager
    )


AuthServiceDepends = Annotated[AuthService, Depends(get_auth_service)]