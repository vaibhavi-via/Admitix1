"""Domain-specific exceptions for the `applications` module (applications,
application preferences, application status history)."""

from __future__ import annotations

from fastapi import HTTPException, status


class ApplicationNotFoundException(HTTPException):
    """Raised when an application id does not exist."""

    def __init__(self, detail: str = "Application not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateApplicationException(HTTPException):
    """Raised when a student already has an application in the given
    cycle — mirrors `uq_applications_student_cycle`."""

    def __init__(
        self, detail: str = "This student already has an application in this admission cycle."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidApplicationStatusTransitionException(HTTPException):
    """Raised when a requested `current_status` change is not a valid
    transition from the application's current state (e.g. moving a
    `cancelled` application back to `submitted`)."""

    def __init__(
        self, detail: str = "This status transition is not allowed."
    ) -> None:
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ApplicationPreferenceNotFoundException(HTTPException):
    """Raised when a referenced application preference does not exist."""

    def __init__(self, detail: str = "Application preference not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicatePreferenceException(HTTPException):
    """Raised when a (application_id, preference_no) or
    (application_id, course_id) pair already exists — mirrors
    `uq_app_preferences_app_order` / `uq_app_preferences_app_course`."""

    def __init__(
        self, detail: str = "This preference order or course has already been added."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class MultipleAllottedPreferencesException(HTTPException):
    """Raised when marking a preference `allotted` would give an
    application more than one allotted preference — mirrors the
    partial unique index `uq_app_preferences_one_allotted`."""

    def __init__(
        self, detail: str = "An application may have at most one allotted preference."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
