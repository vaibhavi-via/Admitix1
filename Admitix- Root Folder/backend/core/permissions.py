"""Reusable role-based permission dependency factories."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from fastapi import Depends

from core.authentication import get_current_user
from core.authorization import require_roles


def require_permission(*allowed_roles: str) -> Callable[..., Any]:
    """Create a FastAPI dependency that allows only the named roles."""

    def dependency(current_user: Any = Depends(get_current_user)) -> Any:
        require_roles(current_user, *allowed_roles)
        return current_user

    return dependency
