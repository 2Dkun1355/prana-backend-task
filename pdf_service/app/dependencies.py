from typing import Annotated

import aioboto3
from fastapi import Depends, Request, HTTPException, status

from .core.security import JWTManager
from .schemas import UserFromToken
from .services import PDFService, QueueService


def get_jwt_manager() -> JWTManager:
    """Dependency provider for JWTManager."""
    return JWTManager()


JWTManagerDepends = Annotated[JWTManager, Depends(get_jwt_manager)]


def get_pdf_service() -> PDFService:
    """Dependency provider for PDFService."""
    return PDFService()


PDFServiceDepends = Annotated[PDFService, Depends(get_pdf_service)]


def get_current_user(request: Request, jwt_manager: JWTManagerDepends) -> UserFromToken:
    """
    Extracts and validates the Bearer token from the Authorization header.
    Returns a validated UserFromToken schema.
    """
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )

    token = auth_header.split(" ")[1]
    payload = jwt_manager.decode_token(token)

    return UserFromToken(**payload)


CurrentUserDepends = Annotated[UserFromToken, Depends(get_current_user)]


def get_queue_service() -> QueueService:
    return QueueService(
        session=aioboto3.Session()
    )


QueueServiceDepends = Annotated[QueueService, Depends(get_queue_service)]
