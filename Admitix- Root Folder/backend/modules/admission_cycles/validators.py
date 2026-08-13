"""Validation helpers for admission-cycle inputs."""

from datetime import date


def validate_application_window(application_start: date, application_end: date) -> None:
    if application_end <= application_start:
        raise ValueError("Application end date must be after the start date.")


def validate_academic_year(academic_year: str) -> str:
    if len(academic_year.strip()) < 4:
        raise ValueError("Academic year must be provided.")
    return academic_year.strip()
