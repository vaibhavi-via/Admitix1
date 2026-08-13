"""Validation helpers for admission application inputs."""

from collections.abc import Sequence

from modules.applications.constants import MAX_PREFERENCES


def validate_preferences(course_ids: Sequence[object]) -> None:
    if not course_ids:
        raise ValueError("At least one course preference is required.")
    if len(course_ids) > MAX_PREFERENCES:
        raise ValueError(f"No more than {MAX_PREFERENCES} course preferences are allowed.")
    if len(set(course_ids)) != len(course_ids):
        raise ValueError("Course preferences must not contain duplicates.")


def validate_remarks(remarks: str | None, *, max_length: int = 2_000) -> str | None:
    if remarks is None:
        return None
    value = remarks.strip()
    if len(value) > max_length:
        raise ValueError(f"Remarks cannot exceed {max_length} characters.")
    return value
