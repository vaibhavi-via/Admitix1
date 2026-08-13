"""Domain-specific exceptions for the `students` module (students,
education details, entrance exam scores)."""

from __future__ import annotations

from fastapi import HTTPException, status


class StudentNotFoundException(HTTPException):
    """Raised when a student id does not exist."""

    def __init__(self, detail: str = "Student not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateStudentProfileException(HTTPException):
    """Raised when the given `user_id` already has a student profile —
    mirrors `uq_students_user_id`."""

    def __init__(
        self, detail: str = "A student profile already exists for this user."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class DuplicateAadhaarException(HTTPException):
    """Raised when `aadhaar_no` already exists for another student
    within the same institution — mirrors
    `uq_students_institution_aadhaar`."""

    def __init__(
        self, detail: str = "This Aadhaar number is already registered for another student."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class EducationDetailNotFoundException(HTTPException):
    """Raised when an education detail id does not exist."""

    def __init__(self, detail: str = "Education detail not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class EntranceExamScoreNotFoundException(HTTPException):
    """Raised when an entrance exam score id does not exist."""

    def __init__(self, detail: str = "Entrance exam score not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)
