"""Role and tenant authorization helpers."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any

from fastapi import HTTPException, status


def role_name(user: Any) -> str | None:
    """Read the role name from a loaded user model without assuming its type."""

    role = getattr(user, "role", None)
    return getattr(role, "role_name", None)


def has_any_role(user: Any, allowed_roles: Iterable[str]) -> bool:
    return role_name(user) in set(allowed_roles)


def require_roles(user: Any, *allowed_roles: str) -> None:
    """Raise 403 unless the user holds at least one required role."""

    if not has_any_role(user, allowed_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")


def require_same_institution(user: Any, institution_id: Any) -> None:
    """Enforce tenant ownership, while allowing platform-level users through."""

    user_institution_id = getattr(user, "institution_id", None)
    if user_institution_id is not None and user_institution_id != institution_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-institution access is not allowed.")
