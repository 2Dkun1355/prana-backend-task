from pydantic import BaseModel, EmailStr, Field
from datetime import date


class UserFromToken(BaseModel):
    """
    Schema representing user data extracted from a JWT payload.
    Used for profile PDF generation.
    """
    id: int = Field(..., title="User ID")
    first_name: str = Field(..., title="First name")
    last_name: str = Field(..., title="Last name")
    email: EmailStr = Field(..., title="Email")
    date_of_birth: date = Field(..., title="Date of birth")

