"""Pydantic (v2) schemas for the `payments` resource."""

from __future__ import annotations

import uuid
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from core.enums import PaymentMode, PaymentStatus


class PaymentBase(BaseModel):
    amount_paid: Decimal = Field(..., gt=0, decimal_places=2)
    payment_mode: PaymentMode | None = None
    transaction_id: str | None = Field(None, max_length=100)


class PaymentCreate(PaymentBase):
    application_id: uuid.UUID
    fee_id: uuid.UUID


class PaymentUpdate(BaseModel):
    payment_status: PaymentStatus | None = None
    transaction_id: str | None = Field(None, max_length=100)


class PaymentRead(PaymentBase):
    model_config = ConfigDict(from_attributes=True)

    payment_id: uuid.UUID
    application_id: uuid.UUID
    fee_id: uuid.UUID
    payment_status: PaymentStatus
    payment_date: datetime
