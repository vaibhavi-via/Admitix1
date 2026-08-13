"""Validation helpers for courses, fees, and seats."""

from decimal import Decimal


def validate_capacity(total_seats: int) -> None:
    if total_seats < 0:
        raise ValueError("Seat capacity cannot be negative.")


def validate_fee_amount(amount: Decimal | int | float) -> None:
    if amount < 0:
        raise ValueError("Fee amount cannot be negative.")
