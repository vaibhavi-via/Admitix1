"""Validation helpers for report requests."""

from datetime import date

from modules.reports.constants import SUPPORTED_EXPORT_FORMATS


def validate_export_format(export_format: str) -> str:
    value = export_format.lower().strip()
    if value not in SUPPORTED_EXPORT_FORMATS:
        raise ValueError(f"Export format must be one of: {', '.join(SUPPORTED_EXPORT_FORMATS)}.")
    return value


def validate_date_range(start_date: date | None, end_date: date | None) -> None:
    if start_date and end_date and end_date < start_date:
        raise ValueError("End date cannot be before start date.")
