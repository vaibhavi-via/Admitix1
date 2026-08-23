"""Business logic for the `applications` resource.

The router only exposes plain CRUD on `Application` itself, but the
model layer implies two pieces of derived behaviour that belong here
rather than in the router:

  * `application_number` is generated server-side on create
    (`ApplicationCreate` intentionally excludes it).
  * Every `current_status` transition is recorded into
    `ApplicationStatusHistory` so the audit trail stays populated even
    though there is no dedicated public endpoint for it.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from core.enums import ApplicationCurrentStatus
from core.authorization import require_same_institution, role_name
from modules.students.models import Student
from modules.users.models import User
from .models import Application, ApplicationStatusHistory
from .schema import ApplicationCreate, ApplicationUpdate


def _generate_application_number(db: Session) -> str:
    """Build a unique, human-readable application number.

    Format: `APP-<year>-<8 hex chars>`. Collisions are astronomically
    unlikely, but we guard against them anyway before returning.
    """

    year = datetime.now(timezone.utc).year

    while True:
        candidate = f"APP-{year}-{uuid.uuid4().hex[:8].upper()}"
        exists = (
            db.query(Application)
            .filter(Application.application_number == candidate)
            .first()
        )
        if not exists:
            return candidate


def create_application(db: Session, application_data: ApplicationCreate, current_user: User) -> Application:
    """Create a new (draft) application for a student in a cycle."""

    student = db.get(Student, application_data.student_id)
    if student is None: raise HTTPException(status_code=404, detail="Student not found.")
    require_same_institution(current_user, student.institution_id)
    if role_name(current_user) == "student" and student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You can only create your own application.")
    application = Application(
        **application_data.model_dump(),
        application_number=_generate_application_number(db),
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    # Seed the audit trail with the initial status.
    history = ApplicationStatusHistory(
        application_id=application.application_id,
        old_status=None,
        new_status=application.current_status.value,
    )
    db.add(history)
    db.commit()
    db.refresh(application)

    return application


def get_applications(db: Session, current_user: User) -> list[Application]:
    """Return every application."""

    query = db.query(Application).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "student": query = query.filter(Student.user_id == current_user.user_id)
    return query.order_by(Application.created_at.desc()).all()


def get_application_by_id(db: Session, application_id: uuid.UUID, current_user: User) -> Application:
    """Fetch a single application by id or raise 404."""

    application = (
        db.query(Application)
        .filter(Application.application_id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found.",
        )

    require_same_institution(current_user, application.student.institution_id)
    if role_name(current_user) == "student" and application.student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You cannot access this application.")
    return application


def update_application(
    db: Session,
    application_id: uuid.UUID,
    application_data: ApplicationUpdate,
    current_user: User,
) -> Application:
    """Partially update an application.

    If `current_status` changes, records the transition in
    `ApplicationStatusHistory` alongside `reviewed_by`/`remarks` if
    they were supplied in the same request.
    """

    application = get_application_by_id(db, application_id, current_user)

    update_data = application_data.model_dump(exclude_unset=True)
    incoming_status: ApplicationCurrentStatus | None = update_data.get("current_status")

    old_status = application.current_status.value
    if role_name(current_user) == "student" and incoming_status not in (None, ApplicationCurrentStatus.SUBMITTED): raise HTTPException(status_code=403, detail="Students can only submit an application.")

    for field, value in update_data.items():
        setattr(application, field, value)

    if incoming_status is not None and incoming_status.value != old_status:
        history = ApplicationStatusHistory(
            application_id=application.application_id,
            old_status=old_status,
            new_status=incoming_status.value,
            changed_by=current_user.user_id,
            remarks=update_data.get("remarks"),
        )
        db.add(history)
        from modules.audit_logs.models import AuditLog
        db.add(AuditLog(user_id=current_user.user_id, action="STATUS_CHANGE", table_name="applications", record_id=application.application_id))

    db.commit()
    db.refresh(application)

    return application


def delete_application(db: Session, application_id: uuid.UUID, current_user: User) -> None:
    """Delete an application (cascades to preferences, status history,
    documents, and payments per the model's relationship config)."""

    application = get_application_by_id(db, application_id, current_user)
    if role_name(current_user) == "student": raise HTTPException(status_code=403, detail="Students cannot delete applications.")
    db.delete(application)
    db.commit()


def get_application_status_history(db: Session, current_user: User):
    query = db.query(ApplicationStatusHistory)
    if current_user.institution_id is not None:
        query = query.filter(ApplicationStatusHistory.institution_id == current_user.institution_id)
    return query.order_by(ApplicationStatusHistory.changed_at.desc()).all()


def get_application_status_history_by_id(db: Session, history_id: uuid.UUID, current_user: User):
    history = db.query(ApplicationStatusHistory).filter(ApplicationStatusHistory.history_id == history_id).first()
    if history is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application status history entry not found.")
    if current_user.institution_id is not None and history.institution_id != current_user.institution_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Cross-institution access is not allowed.")
    return history
