from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from .schema import StaffCreate, StaffRead, StaffUpdate
from .service import create_staff, delete_staff, get_staff, get_staff_by_id, update_staff

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("/", response_model=StaffRead, status_code=status.HTTP_201_CREATED)
def create_staff_route(data: StaffCreate, db: Session = Depends(get_db)): return create_staff(db, data)
@router.get("/", response_model=list[StaffRead])
def list_staff_route(db: Session = Depends(get_db)): return get_staff(db)
@router.get("/{staff_id}", response_model=StaffRead)
def get_staff_route(staff_id: UUID, db: Session = Depends(get_db)): return get_staff_by_id(db, staff_id)
@router.patch("/{staff_id}", response_model=StaffRead)
def update_staff_route(staff_id: UUID, data: StaffUpdate, db: Session = Depends(get_db)): return update_staff(db, staff_id, data)
@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_staff_route(staff_id: UUID, db: Session = Depends(get_db)): delete_staff(db, staff_id)
