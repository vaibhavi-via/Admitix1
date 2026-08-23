from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from .schema import (
    FeeStructureCreate, FeeStructureRead, FeeStructureUpdate,
    SeatMatrixCreate, SeatMatrixRead, SeatMatrixUpdate,
)
from .service import (
    create_fee_structure, get_fee_structures, get_fee_structure_by_id,
    update_fee_structure, delete_fee_structure,
    create_seat_matrix, get_seat_matrix, get_seat_matrix_by_id,
    update_seat_matrix, delete_seat_matrix,
)

fee_router = APIRouter(prefix="/fee-structure", tags=["Fee Structure"])
seat_router = APIRouter(prefix="/seat-matrix", tags=["Seat Matrix"])

@fee_router.post("/", response_model=FeeStructureRead, status_code=status.HTTP_201_CREATED)
async def create_fee(data: FeeStructureCreate, db: Session = Depends(get_db)):
    return create_fee_structure(db, data)

@fee_router.get("/", response_model=list[FeeStructureRead])
async def list_fees(db: Session = Depends(get_db)):
    return get_fee_structures(db)

@fee_router.get("/{fee_id}", response_model=FeeStructureRead)
async def get_fee(fee_id: UUID, db: Session = Depends(get_db)):
    return get_fee_structure_by_id(db, fee_id)

@fee_router.patch("/{fee_id}", response_model=FeeStructureRead)
async def patch_fee(fee_id: UUID, data: FeeStructureUpdate, db: Session = Depends(get_db)):
    return update_fee_structure(db, fee_id, data)

@fee_router.delete("/{fee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_fee(fee_id: UUID, db: Session = Depends(get_db)):
    delete_fee_structure(db, fee_id)

@seat_router.post("/", response_model=SeatMatrixRead, status_code=status.HTTP_201_CREATED)
async def create_seat(data: SeatMatrixCreate, db: Session = Depends(get_db)):
    return create_seat_matrix(db, data)

@seat_router.get("/", response_model=list[SeatMatrixRead])
async def list_seats(db: Session = Depends(get_db)):
    return get_seat_matrix(db)

@seat_router.get("/{seat_id}", response_model=SeatMatrixRead)
async def get_seat(seat_id: UUID, db: Session = Depends(get_db)):
    return get_seat_matrix_by_id(db, seat_id)

@seat_router.patch("/{seat_id}", response_model=SeatMatrixRead)
async def patch_seat(seat_id: UUID, data: SeatMatrixUpdate, db: Session = Depends(get_db)):
    return update_seat_matrix(db, seat_id, data)

@seat_router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_seat(seat_id: UUID, db: Session = Depends(get_db)):
    delete_seat_matrix(db, seat_id)
