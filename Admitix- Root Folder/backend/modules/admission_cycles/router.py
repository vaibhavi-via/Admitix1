from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    AdmissionCycleCreate,
    AdmissionCycleRead,
    AdmissionCycleUpdate,
)
from .service import (
    create_admission_cycle,
    get_admission_cycles,
    get_admission_cycle_by_id,
    update_admission_cycle,
    delete_admission_cycle,
)

router = APIRouter(
    prefix="/admission-cycles",
    tags=["Admission Cycles"],
)


@router.post(
    "/",
    response_model=AdmissionCycleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_admission_cycle_route(
    admission_cycle_data: AdmissionCycleCreate,
    db: Session = Depends(get_db),
):
    return create_admission_cycle(db, admission_cycle_data)


@router.get(
    "/",
    response_model=list[AdmissionCycleRead],
)
async def get_admission_cycles_route(
    db: Session = Depends(get_db),
):
    return get_admission_cycles(db)


@router.get(
    "/{admission_cycle_id}",
    response_model=AdmissionCycleRead,
)
async def get_admission_cycle_by_id_route(
    admission_cycle_id: UUID,
    db: Session = Depends(get_db),
):
    return get_admission_cycle_by_id(db, admission_cycle_id)


@router.patch(
    "/{admission_cycle_id}",
    response_model=AdmissionCycleRead,
)
async def update_admission_cycle_route(
    admission_cycle_id: UUID,
    admission_cycle_data: AdmissionCycleUpdate,
    db: Session = Depends(get_db),
):
    return update_admission_cycle(
        db,
        admission_cycle_id,
        admission_cycle_data,
    )


@router.delete(
    "/{admission_cycle_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_admission_cycle_route(
    admission_cycle_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_admission_cycle(db, admission_cycle_id)
