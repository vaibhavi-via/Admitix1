"""Domain-specific exceptions for the `courses` module (courses, fee
structure, seat matrix)."""

from __future__ import annotations

from fastapi import HTTPException, status


class CourseNotFoundException(HTTPException):
    """Raised when a course id does not exist."""

    def __init__(self, detail: str = "Course not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class FeeStructureNotFoundException(HTTPException):
    """Raised when a fee structure id does not exist."""

    def __init__(self, detail: str = "Fee structure not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class SeatMatrixNotFoundException(HTTPException):
    """Raised when a seat matrix row does not exist."""

    def __init__(self, detail: str = "Seat matrix entry not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateSeatMatrixCategoryException(HTTPException):
    """Raised when (course_id, category) already exists — mirrors
    `uq_seat_matrix_course_category`."""

    def __init__(
        self, detail: str = "A seat matrix entry for this course and category already exists."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class SeatCapacityExceededException(HTTPException):
    """Raised when `filled_seats` would exceed `total_seats` — mirrors
    `ck_seat_matrix_filled_within_total`."""

    def __init__(
        self, detail: str = "filled_seats cannot exceed total_seats."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
