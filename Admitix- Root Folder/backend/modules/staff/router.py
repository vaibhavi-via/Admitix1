from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from core.authorization import require_roles
from .schema import StaffCreate, StaffRead, StaffUpdate, StaffAccountCreate, StaffAccountRead
from .service import create_staff, create_staff_account, delete_staff, get_staff, get_staff_by_id, update_staff

router = APIRouter(prefix="/staff", tags=["Staff"])


def _admin(user: CurrentUser):
    require_roles(user, "super_admin", "institution_admin")
    return user


@router.post("/accounts", response_model=StaffAccountRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(_admin)])
def create_staff_account_route(data: StaffAccountCreate, db: Session = Depends(get_db)):
    return create_staff_account(db, data)


@router.post("/", response_model=StaffRead, status_code=status.HTTP_201_CREATED, dependencies=[Depends(_admin)])
def create_staff_route(data: StaffCreate, db: Session = Depends(get_db)):
    return create_staff(db, data)


@router.get("/", response_model=list[StaffRead], dependencies=[Depends(_admin)])
def list_staff_route(db: Session = Depends(get_db)):
    return get_staff(db)


@router.get("/{staff_id}", response_model=StaffRead, dependencies=[Depends(_admin)])
def get_staff_route(staff_id: UUID, db: Session = Depends(get_db)):
    return get_staff_by_id(db, staff_id)


@router.patch("/{staff_id}", response_model=StaffRead, dependencies=[Depends(_admin)])
def update_staff_route(staff_id: UUID, data: StaffUpdate, db: Session = Depends(get_db)):
    return update_staff(db, staff_id, data)


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(_admin)])
def delete_staff_route(staff_id: UUID, db: Session = Depends(get_db)):
    delete_staff(db, staff_id)
