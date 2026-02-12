"""
JWT authentication: create tokens on login, verify on protected routes.
get_current_user is used as a FastAPI dependency for protected endpoints.
"""
from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pymongo.collection import Collection

from config import settings

# Bearer token scheme: client sends "Authorization: Bearer <token>"
security = HTTPBearer(auto_error=False)


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.
    data usually contains {"sub": user_id or email} for identifying the user.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(
        to_encode,
        settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM,
    )


def decode_token(token: str) -> dict | None:
    """Decode and validate JWT. Returns payload dict or None if invalid."""
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
        return payload
    except JWTError:
        return None


def get_current_user(
    users_collection: Collection,
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(security),
    ] = None,
) -> dict:
    """
    FastAPI dependency: require valid JWT and return user document.
    Use in route: current_user: User = Depends(get_current_user).
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = credentials.credentials
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # "sub" (subject) stores the user identifier (we use email)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    user = users_collection.find_one({"email": sub})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    # Convert _id to string for JSON
    user["id"] = str(user["_id"])
    return user
