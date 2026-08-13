"""Validation helpers for student and academic-detail inputs."""

from decimal import Decimal

from modules.students.constants import MAX_PASSING_YEAR, MIN_PASSING_YEAR


def validate_passing_year(year: int) -> None:
    if not MIN_PASSING_YEAR <= year <= MAX_PASSING_YEAR:
        raise ValueError(f"Passing year must be between {MIN_PASSING_YEAR} and {MAX_PASSING_YEAR}.")


def validate_percentage(percentage: Decimal | int | float | None) -> None:
    if percentage is not None and not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")
