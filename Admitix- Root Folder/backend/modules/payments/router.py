from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    PaymentCreate,
    PaymentRead,
    PaymentUpdate,
)
from .service import (
    create_payment,
    get_payments,
    get_payment_by_id,
    update_payment,
    delete_payment,
)

router = APIRouter(
    prefix="/payments",
    tags=["Payments"],
)


@router.post(
    "/",
    response_model=PaymentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_payment_route(
    payment_data: PaymentCreate,
    db: Session = Depends(get_db),
):
    return create_payment(db, payment_data)


@router.get(
    "/",
    response_model=list[PaymentRead],
)
async def get_payments_route(
    db: Session = Depends(get_db),
):
    return get_payments(db)


@router.get(
    "/{payment_id}",
    response_model=PaymentRead,
)
async def get_payment_by_id_route(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    return get_payment_by_id(db, payment_id)


@router.patch(
    "/{payment_id}",
    response_model=PaymentRead,
)
async def update_payment_route(
    payment_id: UUID,
    payment_data: PaymentUpdate,
    db: Session = Depends(get_db),
):
    return update_payment(db, payment_id, payment_data)


@router.delete(
    "/{payment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_payment_route(
    payment_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_payment(db, payment_id)
