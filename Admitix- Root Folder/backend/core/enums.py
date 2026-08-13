"""
Shared enumerations.

Every enum here mirrors a `CHECK (... IN (...))` constraint already
present in `final_schema_sql.sql`. They are used:

  * In SQLAlchemy models via `sa.Enum(MyEnum, native_enum=False, ...)`,
    which stores the value as plain `VARCHAR` + a `CHECK` constraint —
    i.e. it renders to *exactly* the same column type already in the
    database. No schema change, just typed access in Python.
  * In Pydantic schemas for request/response validation.

Values are lowercase strings to match the existing data exactly.
"""

from __future__ import annotations

from enum import Enum


class StrEnum(str, Enum):
    """Base class so enums serialize as their plain string value."""

    def __str__(self) -> str:  # pragma: no cover - trivial
        return str(self.value)


class Gender(StrEnum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"


class AdmissionCycleStatus(StrEnum):
    UPCOMING = "upcoming"
    OPEN = "open"
    CLOSED = "closed"
    ARCHIVED = "archived"


class ApplicationCurrentStatus(StrEnum):
    DRAFT = "draft"
    SUBMITTED = "submitted"
    UNDER_REVIEW = "under_review"
    DOCUMENTS_PENDING = "documents_pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    ADMITTED = "admitted"
    CANCELLED = "cancelled"


class PreferenceStatus(StrEnum):
    PENDING = "pending"
    ALLOTTED = "allotted"
    REJECTED = "rejected"
    WITHDRAWN = "withdrawn"


class DocumentVerificationStatus(StrEnum):
    PENDING = "pending"
    VERIFIED = "verified"
    REJECTED = "rejected"
    REUPLOAD_REQUESTED = "reupload_requested"


class AIVerificationStatus(StrEnum):
    PENDING = "pending"
    PASSED = "passed"
    FAILED = "failed"
    MANUAL_REVIEW = "manual_review"


class PaymentMode(StrEnum):
    ONLINE = "online"
    CASH = "cash"
    CHEQUE = "cheque"
    DD = "dd"
    CARD = "card"
    UPI = "upi"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"


class NotificationType(StrEnum):
    EMAIL = "email"
    SMS = "sms"
    IN_APP = "in_app"
