"""Domain-specific exceptions for the `auth` module."""

from __future__ import annotations

from fastapi import HTTPException, status


class InvalidCredentialsException(HTTPException):
    """Raised when the email/password combination does not match any
    active user (also covers "user not found" so login never leaks
    which part was wrong)."""

    def __init__(self, detail: str = "Invalid email or password.") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class InactiveAccountException(HTTPException):
    """Raised when a user authenticates successfully but their account
    has been deactivated (`is_active = false`)."""

    def __init__(self, detail: str = "This account has been deactivated.") -> None:
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class InvalidTokenException(HTTPException):
    """Raised when a JWT fails signature/expiry validation, or is used
    at the wrong endpoint (e.g. an access token where a refresh token
    is expected)."""

    def __init__(self, detail: str = "Invalid or expired token.") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class AuthenticationRequiredException(HTTPException):
    """Raised when an endpoint requires an authenticated caller (e.g.
    `/auth/me`, `/auth/logout`, `/auth/change-password`) but none was
    resolved from the request."""

    def __init__(self, detail: str = "Authentication required.") -> None:
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class IncorrectCurrentPasswordException(HTTPException):
    """Raised on `/auth/change-password` when `current_password` does
    not match the stored hash."""

    def __init__(self, detail: str = "Current password is incorrect.") -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
