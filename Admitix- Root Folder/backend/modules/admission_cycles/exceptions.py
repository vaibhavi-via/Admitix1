"""Domain-specific exceptions for the `admission_cycles` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class AdmissionCycleNotFoundException(HTTPException):
    """Raised when an admission cycle id does not exist."""

    def __init__(self, detail: str = "Admission cycle not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateAdmissionCycleException(HTTPException):
    """Raised when (institution_id, academic_year) already exists —
    mirrors `uq_admission_cycles_institution_year`."""

    def __init__(
        self, detail: str = "An admission cycle for this academic year already exists."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidAdmissionCycleDateRangeException(HTTPException):
    """Raised when `application_end` is not after `application_start` —
    mirrors `ck_admission_cycles_dates` (also validated in the
    Pydantic schema, but kept here for defense-in-depth at the service
    layer)."""

    def __init__(
        self, detail: str = "application_end must be after application_start."
    ) -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class AdmissionCycleClosedException(HTTPException):
    """Raised when an operation (e.g. new application) is attempted
    against a cycle that is not `open`."""

    def __init__(
        self, detail: str = "This admission cycle is not currently open."
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
