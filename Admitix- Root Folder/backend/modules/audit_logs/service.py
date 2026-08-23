"""Business logic for the `audit_logs` resource.

Audit logs are append-only: the router intentionally exposes no
update or delete endpoints, so this module only implements create and
read operations.
"""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import AuditLog
from .schema import AuditLogCreate


def create_audit_log(db: Session, audit_log_data: AuditLogCreate) -> AuditLog:
    """Record a new audit log entry.

    `institution_id`, when omitted, is left `None` here and populated
    by the `trg_set_audit_log_institution` DB trigger from the acting
    user's institution.
    """

    audit_log = AuditLog(**audit_log_data.model_dump())

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


def get_audit_logs(db: Session, current_user=None) -> list[AuditLog]:
    """Return every audit log entry, most recent first."""

    query = db.query(AuditLog)
    if current_user is not None and current_user.institution_id is not None:
        query = query.filter(AuditLog.institution_id == current_user.institution_id)
    return query.order_by(AuditLog.created_at.desc()).all()


def get_audit_log_by_id(db: Session, audit_log_id: uuid.UUID, current_user=None) -> AuditLog:
    """Fetch a single audit log entry by id or raise 404."""

    audit_log = db.query(AuditLog).filter(AuditLog.log_id == audit_log_id).first()

    if audit_log is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Audit log entry not found.",
        )

    return audit_log
