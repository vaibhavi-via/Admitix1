from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .schema import PaymentCreate, PaymentRead, PaymentUpdate
from .service import create_payment, get_payments, get_payment_by_id, update_payment, delete_payment
router = APIRouter(prefix="/payments", tags=["Payments"])
@router.post("/", response_model=PaymentRead, status_code=status.HTTP_201_CREATED)
def create_payment_route(payment_data: PaymentCreate, current_user: CurrentUser, db: Session = Depends(get_db)): return create_payment(db, payment_data, current_user)
@router.get("/", response_model=list[PaymentRead])
def get_payments_route(current_user: CurrentUser, db: Session = Depends(get_db)): return get_payments(db, current_user)
@router.get("/{payment_id}", response_model=PaymentRead)
def get_payment_by_id_route(payment_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): return get_payment_by_id(db, payment_id, current_user)
@router.patch("/{payment_id}", response_model=PaymentRead)
def update_payment_route(payment_id: UUID, payment_data: PaymentUpdate, current_user: CurrentUser, db: Session = Depends(get_db)): return update_payment(db, payment_id, payment_data, current_user)
@router.delete("/{payment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_payment_route(payment_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): return delete_payment(db, payment_id, current_user)
