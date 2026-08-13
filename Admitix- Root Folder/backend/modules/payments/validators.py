"""Validation helpers for payment inputs."""

from decimal import Decimal


def validate_amount(amount: Decimal | int | float) -> None:
    if amount <= 0:
        raise ValueError("Payment amount must be greater than zero.")


def validate_transaction_id(transaction_id: str | None) -> str | None:
    if transaction_id is None:
        return None
    value = transaction_id.strip()
    if not value:
        raise ValueError("Transaction ID cannot be blank when supplied.")
    return value
