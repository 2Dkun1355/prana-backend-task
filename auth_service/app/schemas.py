from pydantic import BaseModel, EmailStr, Field
from datetime import date


class UserBase(BaseModel):
    """
    Base schema for User data, enabling ORM mode for SQLAlchemy compatibility.
    """
    first_name: str = Field(..., title="First name")
    last_name: str = Field(..., title="Last name")
    email: EmailStr = Field(..., title="Email")
    date_of_birth: date = Field(..., title="Date of birth")

    model_config = {
        "from_attributes": True
    }


class UserResponse(UserBase):
    """
    Schema for user profile data returned in API responses.
    """
    id: int = Field(..., title="User ID")

class UserCreate(UserBase):
    """
    Schema for user registration, including password.
    Note: 'id' is excluded during actual creation in the service layer.
    """
    password: str = Field(..., title="Password")


class UserAuth(BaseModel):
    """
    Schema for user authentication (login).
    """
    email: EmailStr = Field(..., title="Email")
    password: str = Field(..., title="Password")


class TokenResponse(BaseModel):
    """
    Schema for successful authentication response containing JWT.
    """
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field("Bearer", description="Token type, always 'bearer'")
