"""Password and JWT primitives used by authentication-related code."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import ALGORITHM, SECRET_KEY


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return password_context.verify(plain_password, password_hash)


def create_token(payload: dict[str, Any], *, expires_delta: timedelta) -> str:
    """Encode a JWT without mutating the caller's payload."""

    now = datetime.now(timezone.utc)
    claims = {**payload, "iat": now, "exp": now + expires_delta}
    return jwt.encode(claims, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any] | None:
    """Decode a JWT, returning ``None`` for an invalid or expired token."""

    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None
