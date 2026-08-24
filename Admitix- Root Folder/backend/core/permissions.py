"""Reusable role-based permission dependency factories."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import Any

from fastapi import Depends, HTTPException, Request, status

from core.authentication import get_current_user
from core.authorization import require_roles


def require_permission(*allowed_roles: str) -> Callable[..., Any]:
    """Create a FastAPI dependency that allows only the named roles."""

    def dependency(current_user: Any = Depends(get_current_user)) -> Any:
        require_roles(current_user, *allowed_roles)
        return current_user

    return dependency


def require_module_access(
    read_roles: Iterable[str],
    write_roles: Iterable[str] | None = None,
) -> Callable[..., Any]:
    """Enforce RBAC at router level without changing existing endpoint signatures.

    GET/HEAD requests use ``read_roles``. Mutating requests use ``write_roles``.
    This is deliberately kept separate from ownership checks, which belong in
    the service layer where the target record is available.
    """

    read = frozenset(read_roles)
    write = frozenset(write_roles if write_roles is not None else read)

    def dependency(
        request: Request,
        current_user: Any = Depends(get_current_user),
    ) -> Any:
        method = request.method.upper()
        allowed = read if method in {"GET", "HEAD", "OPTIONS"} else write
        if getattr(current_user, "role_name", None) not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation.",
            )
        return current_user

    return dependency
