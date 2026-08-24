"""Role and tenant authorization helpers."""

from __future__ import annotations
from collections.abc import Iterable
from typing import Any
from fastapi import HTTPException, status


def role_name(user: Any) -> str | None:
    role = getattr(user, "role", None)
    return getattr(role, "role_name", None)


def has_any_role(user: Any, allowed_roles: Iterable[str]) -> bool:
    return role_name(user) in set(allowed_roles)


def require_roles(user: Any, *allowed_roles: str) -> None:
    if not has_any_role(user, allowed_roles):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions.")


def require_same_institution(user: Any, institution_id: Any) -> None:
    user_institution_id = getattr(user, "institution_id", None)
    if user_institution_id is not None and user_institution_id != institution_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-institution access is not allowed.")


def require_own_student(user: Any, student: Any) -> None:
    """Allow admin/officer users through; a student may only access own profile."""
    if role_name(user) == "student" and getattr(student, "user_id", None) != getattr(user, "user_id", None):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can only access your own student records.")
