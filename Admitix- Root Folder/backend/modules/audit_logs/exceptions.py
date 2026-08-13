"""Domain-specific exceptions for the `audit_logs` resource.

Audit logs are append-only (create + read only), so there are no
update/delete-conflict exceptions here — only lookup failures.
"""

from __future__ import annotations

from fastapi import HTTPException, status


class AuditLogNotFoundException(HTTPException):
    """Raised when an audit log id does not exist."""

    def __init__(self, detail: str = "Audit log entry not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
