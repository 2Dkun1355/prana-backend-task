import logging
from .repository import UserRepository
from .schemas import UserCreate, UserResponse, UserAuth
from .core.security import PasswordManager, JWTManager

logger = logging.getLogger(__name__)


class AuthService:
    """
    Orchestrates user-related business logic, including registration and authentication.
    """

    def __init__(
            self,
            repository: UserRepository,
            password_manager: PasswordManager,
            jwt_manager: JWTManager
    ):
        self.repository = repository
        self.password_manager = password_manager
        self.jwt_manager = jwt_manager

    async def create_account(self, user_data: UserCreate) -> UserResponse:
        """
        Handles new user registration: checks email uniqueness, hashes password, 
        and persists user data.
        """
        try:
            existing_user = await self.repository.get_by_email(email=user_data.email)
            if existing_user:
                raise ValueError("Email must be unique")

            hashed_password = self.password_manager.hash(user_data.password)

            user_dict = user_data.model_dump(exclude={"id"})
            user_dict["password"] = hashed_password

            user = await self.repository.create(**user_dict)
            logger.info(f"User registered: {user.email}")
            return UserResponse.from_orm(user)

        except Exception as e:
            logger.error(f"Signup error: {e}")
            raise RuntimeError("Could not create account")

    async def authenticate(self, auth_data: UserAuth) -> str:
        """
        Validates user credentials and returns a JWT token containing profile data.
        """
        try:
            user = await self.repository.get_by_email(email=auth_data.email)

            if not user or not self.password_manager.verify(
                    password=auth_data.password,
                    hashed_password=user.password
            ):
                raise ValueError("Incorrect email or password")

            user_payload = UserResponse.from_orm(user).model_dump(mode='json')

            access_token = self.jwt_manager.create_token(data=user_payload)
            return access_token

        except Exception as e:
            logger.error(f"Login error: {e}")
            raise RuntimeError("Authentication failed")
