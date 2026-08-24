"""Pydantic schemas for authentication and account activation."""

from __future__ import annotations

import uuid

from pydantic import BaseModel, EmailStr, Field

from modules.users.schema import UserRead


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    institution_code: str | None = Field(None, max_length=20)


class RegisterRequest(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    phone: str | None = Field(None, max_length=20)
    institution_code: str = Field(..., min_length=2, max_length=20)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token TTL, in seconds")
    user: UserRead


class LoginResponse(TokenResponse):
    pass


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(..., min_length=8, max_length=128)
    new_password: str = Field(..., min_length=8, max_length=128)


class StaffOtpRequest(BaseModel):
    email: EmailStr
    institution_code: str = Field(..., min_length=2, max_length=20)


class StaffOtpResponse(BaseModel):
    message: str
    expires_in_seconds: int
    # Present only for local/demo setups when SMTP is not configured.
    dev_otp: str | None = None
    challenge_token: str


class StaffOtpVerifyRequest(BaseModel):
    email: EmailStr
    institution_code: str = Field(..., min_length=2, max_length=20)
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^\d{6}$")
    challenge_token: str = Field(..., min_length=20)
    new_password: str = Field(..., min_length=8, max_length=128)


class ActivateAccountRequest(BaseModel):
    activation_token: str = Field(..., min_length=20)
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
    user_id: uuid.UUID
    institution_id: uuid.UUID | None
    role_id: uuid.UUID
