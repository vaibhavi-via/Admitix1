"""Domain-specific exceptions for the `users` module (users, staff)."""

from __future__ import annotations

from fastapi import HTTPException, status


class UserNotFoundException(HTTPException):
    """Raised when a user id does not exist."""

    def __init__(self, detail: str = "User not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateEmailException(HTTPException):
    """Raised when `email` already belongs to another user within the
    same institution (or another Super Admin, when `institution_id` is
    `None`) — mirrors `uq_users_institution_email` /
    `uq_users_super_admin_email`."""

    def __init__(
        self, detail: str = "This email is already in use for this institution."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class StaffNotFoundException(HTTPException):
    """Raised when a staff profile id does not exist."""

    def __init__(self, detail: str = "Staff profile not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateStaffProfileException(HTTPException):
    """Raised when the given `user_id` already has a staff profile."""

    def __init__(
        self, detail: str = "A staff profile already exists for this user."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class DuplicateEmployeeIdException(HTTPException):
    """Raised when `employee_id` already exists for another staff
    member."""

    def __init__(self, detail: str = "This employee id is already in use.") -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
