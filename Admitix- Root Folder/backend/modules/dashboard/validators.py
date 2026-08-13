"""Validation helpers for dashboard query parameters."""

from modules.dashboard.constants import MAX_RECENT_ITEMS_LIMIT


def validate_recent_items_limit(limit: int) -> int:
    if not 1 <= limit <= MAX_RECENT_ITEMS_LIMIT:
        raise ValueError(f"Limit must be between 1 and {MAX_RECENT_ITEMS_LIMIT}.")
    return limit
