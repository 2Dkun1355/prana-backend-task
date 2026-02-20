from datetime import datetime, timedelta, timezone
from typing import Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import settings

class PasswordManager:
    """
    Handles secure password hashing and verification using the Argon2 algorithm.
    """
    def __init__(self):
        # Argon2 is the winner of the Password Hashing Competition (PHC)
        self.pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

    def hash(self, password: str) -> str:
        """Generates a secure hash from a plain-text password."""
        return self.pwd_context.hash(password)

    def verify(self, password: str, hashed_password: str) -> bool:
        """Verifies a plain-text password against a stored hash."""
        return self.pwd_context.verify(password, hashed_password)


class JWTManager:
    """
    Provides methods to encode and decode JSON Web Tokens (JWT).
    Designed to work across microservices without a shared database.
    """
    def __init__(
        self,
        secret_key: str = settings.SECRET_KEY,
        algorithm: str = settings.ALGORITHM,
        expire_minutes: int = settings.ACCESS_TOKEN_EXPIRE_MINUTES
    ):
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.access_expire_minutes = expire_minutes

    def create_token(self, data: Dict[str, Any]) -> str:
        """
        Creates a signed JWT token containing user profile data.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=self.access_expire_minutes)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodes and validates a JWT token.
        Options are set to avoid common 'Incorrect claims' errors in microservices.
        """
        try:
            # We ignore aud/iss checks to allow flexible communication between services
            options = {"verify_aud": False, "verify_iss": False}
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                options=options
            )
            return payload
        except JWTError as e:
            # Re-raising or handling the error is crucial for the security layer
            raise e