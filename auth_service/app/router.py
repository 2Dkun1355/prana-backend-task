from fastapi import APIRouter, HTTPException, status
from .schemas import UserCreate, UserResponse, UserAuth, TokenResponse
from .dependencies import AuthServiceDepends

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
            detail={"error": "Registration Error", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Server Error", "message": "An unexpected error occurred"}
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
            detail={"error": "Auth Error", "message": str(e)}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Server Error", "message": "Internal server error"}
        )