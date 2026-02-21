import uuid
from pydantic import BaseModel, EmailStr, Field
from datetime import date


class UserFromToken(BaseModel):
    """
    Schema representing user data extracted from a JWT payload.
    Used for profile PDF generation.
    """
    id: uuid.UUID = Field(..., title="User ID")
    name: str = Field(..., title="Name")
    surname: str = Field(..., title="Surname")
    email: EmailStr = Field(..., title="Email")
    date_of_birth: date = Field(..., title="Date of birth")

