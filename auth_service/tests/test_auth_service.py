import pytest
from unittest.mock import AsyncMock, MagicMock
from app.services import AuthService
from app.schemas import UserCreate, UserAuth
from datetime import date


@pytest.fixture
def auth_service():
    repository = AsyncMock()
    password_manager = MagicMock()
    jwt_manager = MagicMock()

    service = AuthService(
        repository=repository,
        password_manager=password_manager,
        jwt_manager=jwt_manager
    )
    return service, repository, password_manager, jwt_manager


@pytest.mark.asyncio
async def test_create_account_success(auth_service):
    service, repo, pwd_manager, _ = auth_service

    user_data = UserCreate(
        first_name="Ivan", last_name="Dev", email="new@test.com",
        password="plain_password", date_of_birth=date(1990, 1, 1)
    )

    repo.get_by_email.return_value = None
    pwd_manager.hash.return_value = "hashed_password"
    repo.create.return_value = MagicMock(
        id=1, **user_data.model_dump(exclude={"password"}), password="hashed_password"
    )

    result = await service.create_account(user_data)

    assert result.email == user_data.email
    pwd_manager.hash.assert_called_once_with("plain_password")
    repo.create.assert_called_once()


@pytest.mark.asyncio
async def test_create_account_duplicate_email(auth_service):
    service, repo, _, _ = auth_service
    user_data = UserCreate(
        first_name="Ivan", last_name="Dev", email="exists@test.com",
        password="password", date_of_birth=date(1990, 1, 1)
    )

    repo.get_by_email.return_value = {"id": 1, "email": "exists@test.com"}

    with pytest.raises(ValueError, match="Email must be unique"):
        await service.create_account(user_data)


@pytest.mark.asyncio
async def test_authenticate_success(auth_service):
    service, repo, pwd_manager, jwt_man = auth_service
    auth_data = UserAuth(email="test@test.com", password="right_password")

    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.first_name = "Ivan"
    mock_user.last_name = "Test"
    mock_user.email = "test@test.com"
    mock_user.password = "hashed_in_db"
    mock_user.date_of_birth = date(1990, 1, 1)

    repo.get_by_email.return_value = mock_user
    pwd_manager.verify.return_value = True
    jwt_man.create_token.return_value = "fake_jwt_token"

    token = await service.authenticate(auth_data)

    assert token == "fake_jwt_token"


@pytest.mark.asyncio
async def test_authenticate_invalid_password(auth_service):
    service, repo, pwd_manager, _ = auth_service
    auth_data = UserAuth(email="test@test.com", password="wrong_password")

    repo.get_by_email.return_value = MagicMock(password="hashed_in_db")
    pwd_manager.verify.return_value = False

    with pytest.raises(ValueError, match="Incorrect email or password"):
        await service.authenticate(auth_data)