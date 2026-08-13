"""Domain-specific exceptions for the `roles` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class RoleNotFoundException(HTTPException):
    """Raised when a role id does not exist."""

    def __init__(self, detail: str = "Role not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateRoleNameException(HTTPException):
    """Raised when `role_name` already exists — mirrors the `unique`
    constraint on `roles.role_name`."""

    def __init__(self, detail: str = "This role already exists.") -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class RoleInUseException(HTTPException):
    """Raised when attempting to delete a role that is still assigned
    to existing users (`users.role_id` is `ON DELETE RESTRICT`)."""

    def __init__(
        self, detail: str = "This role is assigned to existing users and cannot be deleted."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
