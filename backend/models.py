"""
Pydantic models for request/response validation.
Used by FastAPI for automatic validation and OpenAPI docs.
"""
from pydantic import BaseModel, EmailStr


# ---------- Auth ----------
class UserRegister(BaseModel):
    """Payload for POST /register."""

    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Payload for POST /login."""

    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response after successful login."""

    access_token: str
    token_type: str = "bearer"
    message: str = "Login success"


class UserOut(BaseModel):
    """User data returned to client (no password)."""

    email: str
    id: str | None = None  # MongoDB _id as string

    class Config:
        from_attributes = True
