"""Validation helpers for AI verification results."""

from decimal import Decimal

from modules.ai_verification.constants import MAX_CONFIDENCE_SCORE, MIN_CONFIDENCE_SCORE


def validate_score(score: Decimal | float | int | None, field_name: str) -> None:
    if score is not None and not MIN_CONFIDENCE_SCORE <= score <= MAX_CONFIDENCE_SCORE:
        raise ValueError(f"{field_name} must be between 0 and 100.")
