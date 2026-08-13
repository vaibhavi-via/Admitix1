"""
Central SQLAlchemy declarative base + metadata naming convention.

Every model in `modules/*/models.py` inherits from `Base` defined here.
This module is also the single place that imports every ORM model so
that:

  1. `Base.metadata` is fully populated for Alembic autogeneration
     (`alembic revision --autogenerate` walks `Base.metadata`).
  2. `relationship(..., "ClassName")` string references can resolve
     across modules regardless of import order elsewhere in the app.

Import this module (or anything that imports it, e.g. `db.session`)
before creating tables or running Alembic.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase

# Consistent constraint naming convention -> predictable Alembic
# migration diffs and easier debugging of FK/CHECK/UNIQUE violations.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Declarative base shared by every ORM model in the project."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


# ---------------------------------------------------------------------------
# Import every module's models so they register on `Base.metadata`.
# Keep this list alphabetical and in sync with `modules/`.
#
# Fix note: avoid eager symbol resolution from `db.base` during a re-entrant
# model import. The registry now resolves model classes lazily, so the
# module graph can finish initializing without asking for a partially
# initialized `Institution` symbol while `modules.institutions.models` is
# still importing `db.base`.
# ---------------------------------------------------------------------------
from importlib import import_module

if TYPE_CHECKING:
    from modules.admission_cycles.models import AdmissionCycle
    from modules.ai_verification.models import AIVerification
    from modules.applications.models import (
        Application,
        ApplicationPreference,
        ApplicationStatusHistory,
    )
    from modules.audit_logs.models import AuditLog
    from modules.chat.models import ChatHistory
    from modules.courses.models import Course, FeeStructure, SeatMatrix
    from modules.departments.models import Department
    from modules.document_types.models import DocumentType
    from modules.documents.models import Document
    from modules.faculties.models import Faculty
    from modules.institutions.models import Institution
    from modules.notifications.models import Notification
    from modules.payments.models import Payment
    from modules.roles.models import Role
    from modules.students.models import EducationDetail, EntranceExamScore, Student
    from modules.users.models import Staff, User


_MODEL_IMPORTS = {
    "AdmissionCycle": "modules.admission_cycles.models",
    "AIVerification": "modules.ai_verification.models",
    "Application": "modules.applications.models",
    "ApplicationPreference": "modules.applications.models",
    "ApplicationStatusHistory": "modules.applications.models",
    "AuditLog": "modules.audit_logs.models",
    "ChatHistory": "modules.chat.models",
    "Course": "modules.courses.models",
    "FeeStructure": "modules.courses.models",
    "SeatMatrix": "modules.courses.models",
    "Department": "modules.departments.models",
    "DocumentType": "modules.document_types.models",
    "Document": "modules.documents.models",
    "Faculty": "modules.faculties.models",
    "Institution": "modules.institutions.models",
    "Notification": "modules.notifications.models",
    "Payment": "modules.payments.models",
    "Role": "modules.roles.models",
    "EducationDetail": "modules.students.models",
    "EntranceExamScore": "modules.students.models",
    "Student": "modules.students.models",
    "Staff": "modules.users.models",
    "User": "modules.users.models",
}


def __getattr__(name: str):
    """Resolve model symbols lazily so metadata registration does not re-enter a partially initialized module."""

    if name in _MODEL_IMPORTS:
        module = import_module(_MODEL_IMPORTS[name])
        return getattr(module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = [
    "Base",
    "AdmissionCycle",
    "AIVerification",
    "Application",
    "ApplicationPreference",
    "ApplicationStatusHistory",
    "AuditLog",
    "ChatHistory",
    "Course",
    "FeeStructure",
    "SeatMatrix",
    "Department",
    "DocumentType",
    "Document",
    "Faculty",
    "Institution",
    "Notification",
    "Payment",
    "Role",
    "EducationDetail",
    "EntranceExamScore",
    "Student",
    "Staff",
    "User",
]
