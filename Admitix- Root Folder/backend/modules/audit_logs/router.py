from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from core.authentication import CurrentUser

from .schema import (
    AuditLogCreate,
    AuditLogRead,
)
from .service import (
    create_audit_log,
    get_audit_logs,
    get_audit_log_by_id,
)

router = APIRouter(
    prefix="/audit-logs",
    tags=["Audit Logs"],
)


@router.post(
    "/",
    response_model=AuditLogRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_audit_log_route(
    audit_log_data: AuditLogCreate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return create_audit_log(db, audit_log_data)


@router.get(
    "/",
    response_model=list[AuditLogRead],
)
async def get_audit_logs_route(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return get_audit_logs(db, current_user)


@router.get(
    "/{audit_log_id}",
    response_model=AuditLogRead,
)
async def get_audit_log_by_id_route(
    audit_log_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return get_audit_log_by_id(db, audit_log_id, current_user)
