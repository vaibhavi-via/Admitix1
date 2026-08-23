"""Business logic for the `auth` module.

There is no dedicated ORM model for authentication (see
`modules.auth.models`); this module operates directly on
`modules.users.models.User` and issues stateless JWTs.

Note on `logout_user` / `change_password` / `get_current_user_profile`:
the current router does not yet wire a `get_current_user` dependency
that resolves the caller's identity from the `Authorization` header
(see `core/authentication.py`, currently empty). These three functions
therefore accept an optional `current_user_id` keyword — defaulting to
`None` so the existing router call sites (`change_password(db,
password_data)`, etc.) keep working unmodified — and raise 401 until
that dependency is added to the router.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from sqlalchemy import func

from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, SECRET_KEY
from modules.institutions.models import Institution
from modules.users.models import User
from modules.students.models import Student
from modules.roles.models import Role

from .schema import ChangePasswordRequest, LoginRequest, RefreshTokenRequest, RegisterRequest, TokenResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

REFRESH_TOKEN_EXPIRE_DAYS = 7


# ---------------------------------------------------------------------------
# Password helpers
# ---------------------------------------------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


# ---------------------------------------------------------------------------
# Token helpers
# ---------------------------------------------------------------------------
def _create_token(user: User, expires_delta: timedelta, token_type: str) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.user_id),
        "institution_id": str(user.institution_id) if user.institution_id else None,
        "role_id": str(user.role_id),
        "type": token_type,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(user: User) -> str:
    return _create_token(
        user, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES), token_type="access"
    )


def create_refresh_token(user: User) -> str:
    return _create_token(
        user, timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS), token_type="refresh"
    )


def decode_token(token: str, expected_type: str | None = None) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
        )

    if expected_type and payload.get("type") != expected_type:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type.",
        )

    return payload


# ---------------------------------------------------------------------------
# Service functions
# ---------------------------------------------------------------------------

def register_student(db: Session, data: RegisterRequest) -> TokenResponse:
    institution = db.query(Institution).filter(func.upper(Institution.institution_code) == data.institution_code.strip().upper()).first()
    if institution is None or not institution.status:
        raise HTTPException(status_code=400, detail="Invalid or inactive institution code.")
    if db.query(User).filter(User.institution_id == institution.institution_id, User.email == data.email).first():
        raise HTTPException(status_code=409, detail="An account with this email already exists for this institution.")
    role = db.query(Role).filter(Role.role_name == "student").first()
    if role is None:
        role = Role(role_name="student", description="Student applicant")
        db.add(role); db.flush()
    user = User(institution_id=institution.institution_id, role_id=role.role_id, first_name=data.first_name.strip(), last_name=data.last_name.strip() if data.last_name else None, email=data.email, phone=data.phone, password_hash=hash_password(data.password), is_active=True)
    db.add(user); db.flush()
    db.add(Student(user_id=user.user_id, institution_id=institution.institution_id))
    db.commit(); db.refresh(user)
    return TokenResponse(access_token=create_access_token(user), refresh_token=create_refresh_token(user), expires_in=ACCESS_TOKEN_EXPIRE_MINUTES*60, user=user)


def login_user(db: Session, login_data: LoginRequest) -> TokenResponse:
    """Authenticate a user by email (+ optional institution_code) and
    password, and issue an access/refresh token pair."""

    query = db.query(User).filter(User.email == login_data.email)

    if login_data.institution_code:
        query = query.join(Institution, User.institution_id == Institution.institution_id).filter(
            Institution.institution_code == login_data.institution_code
        )
    else:
        query = query.filter(User.institution_id.is_(None))

    user = query.first()

    if user is None or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account has been deactivated.",
        )

    user.last_login = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


def refresh_access_token(db: Session, refresh_data: RefreshTokenRequest) -> TokenResponse:
    """Exchange a valid refresh token for a new access/refresh pair."""

    payload = decode_token(refresh_data.refresh_token, expected_type="refresh")

    user = db.query(User).filter(User.user_id == uuid.UUID(payload["sub"])).first()

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User no longer exists or is inactive.",
        )

    return TokenResponse(
        access_token=create_access_token(user),
        refresh_token=create_refresh_token(user),
        expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=user,
    )


def logout_user(db: Session, current_user_id: uuid.UUID | None = None) -> dict:
    """Log the current user out.

    Tokens here are stateless JWTs with no server-side session/
    blacklist table, so logout is a client-side action (discard the
    tokens). This endpoint exists as a hook for that future blacklist
    table and to validate that a caller is authenticated.
    """

    if current_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    return {"detail": "Successfully logged out."}


def change_password(
    db: Session,
    password_data: ChangePasswordRequest,
    current_user_id: uuid.UUID | None = None,
) -> dict:
    """Change the current user's password after verifying the old one."""

    if current_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    user = db.query(User).filter(User.user_id == current_user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    if not verify_password(password_data.current_password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect.",
        )

    user.password_hash = hash_password(password_data.new_password)
    db.commit()

    return {"detail": "Password changed successfully."}


def get_current_user_profile(db: Session, current_user_id: uuid.UUID | None = None) -> User:
    """Return the profile of the currently authenticated user."""

    if current_user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required.",
        )

    user = db.query(User).filter(User.user_id == current_user_id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found."
        )

    return user
