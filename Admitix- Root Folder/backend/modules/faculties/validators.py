"""Validation helpers for faculty records."""

from modules.faculties.constants import FACULTY_CODE_MAX_LENGTH


def validate_faculty_code(code: str) -> str:
    value = code.strip().upper()
    if not value:
        raise ValueError("Faculty code is required.")
    if len(value) > FACULTY_CODE_MAX_LENGTH:
        raise ValueError(f"Faculty code cannot exceed {FACULTY_CODE_MAX_LENGTH} characters.")
    return value
