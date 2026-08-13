"""Pydantic (v2) schemas for the `auth` module.

No dedicated table backs this module — it authenticates against
`modules.users.models.User`. These schemas cover login, token issuance
and password-change flows only.
"""

from __future__ import annotations

import uuid

from pydantic import BaseModel, EmailStr, Field

from modules.users.schema import UserRead


class LoginRequest(BaseModel):
    """Payload for `POST /auth/login`.

    `institution_code` disambiguates which tenant to authenticate
    against when the same email is reused across institutions (see
    the partial-unique-index design on `users.email`). Omit it only
    when authenticating a platform-level Super Admin.
    """

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    institution_code: str | None = Field(None, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token TTL, in seconds")
    user: UserRead


# Backward-compatible alias used by older router/service imports.
class LoginResponse(TokenResponse):
    pass


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)


class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    institution_code: str | None = Field(None, max_length=20)


class ResetPasswordRequest(BaseModel):
    reset_token: str
    new_password: str = Field(..., min_length=8, max_length=128)


class LogoutRequest(BaseModel):
    refresh_token: str


class AuthenticatedUser(BaseModel):
    """Lightweight identity payload decoded from a validated JWT, used
    by `core.authentication` / FastAPI dependencies — not an ORM
    read-model."""

    user_id: uuid.UUID
    institution_id: uuid.UUID | None
    role_id: uuid.UUID
