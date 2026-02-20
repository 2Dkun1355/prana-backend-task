from fastapi import APIRouter, HTTPException, status
from app.schemas import UserCreate, UserResponse, UserAuth, TokenResponse
from app.dependencies import AuthServiceDepends

auth_router = APIRouter(prefix="/api/auth", tags=["auth"])

@auth_router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def signup(
    user_data: UserCreate,
    service: AuthServiceDepends
):
    """
    Registers a new user account in the system.
    """
    try:
        return await service.create_account(user_data=user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@auth_router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK
)
async def login(
    auth_data: UserAuth,
    service: AuthServiceDepends
):
    """
    Authenticates a user and returns a profile-encoded JWT access token.
    """
    try:
        access_token = await service.authenticate(auth_data=auth_data)
        return {"access_token": access_token, "token_type": "Bearer"}
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )