from fastapi import HTTPException, status
from jose import jwt
from jose.exceptions import JWTClaimsError, ExpiredSignatureError, JWTError
from .config import settings


class JWTManager:
    """
    Manager for handling JWT decoding and validation.
    """

    def __init__(self, secret_key: str = settings.SECRET_KEY, algorithm: str = settings.ALGORITHM):
        self.secret_key = secret_key
        self.algorithm = algorithm

    def decode_token(self, token: str) -> dict:
        """
        Decodes a JWT token and returns its payload.

        Raises:
            HTTPException: 401 if token is expired, has invalid claims, or is malformed.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except JWTClaimsError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect claims, check audience or issuer"
            )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )