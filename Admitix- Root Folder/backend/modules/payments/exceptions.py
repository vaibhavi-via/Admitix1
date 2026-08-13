"""Domain-specific exceptions for the `payments` resource."""

from __future__ import annotations

from fastapi import HTTPException, status


class PaymentNotFoundException(HTTPException):
    """Raised when a payment id does not exist."""

    def __init__(self, detail: str = "Payment not found.") -> None:
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class DuplicateTransactionIdException(HTTPException):
    """Raised when `transaction_id` has already been recorded against
    another payment — mirrors `uq_payments_transaction_id`."""

    def __init__(
        self, detail: str = "This transaction id has already been recorded."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class InvalidPaymentAmountException(HTTPException):
    """Raised when `amount_paid` is not strictly positive — mirrors
    `ck_payments_amount_paid`."""

    def __init__(self, detail: str = "amount_paid must be greater than zero.") -> None:
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=detail)


class PaymentAlreadyFinalizedException(HTTPException):
    """Raised when attempting to modify a payment that is already in a
    terminal status (`success`, `refunded`)."""

    def __init__(
        self, detail: str = "This payment has already been finalized and cannot be changed."
    ) -> None:
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)
