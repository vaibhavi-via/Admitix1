from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    InstitutionCreate,
    InstitutionRead,
    InstitutionUpdate,
)
from .service import (
    create_institution,
    get_institutions,
    get_institution_by_id,
    update_institution,
    delete_institution,
)

router = APIRouter(
    prefix="/institutions",
    tags=["Institutions"],
)


@router.post(
    "/",
    response_model=InstitutionRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_institution_route(
    institution_data: InstitutionCreate,
    db: Session = Depends(get_db),
):
    return create_institution(db, institution_data)


@router.get(
    "/",
    response_model=list[InstitutionRead],
)
async def get_institutions_route(
    db: Session = Depends(get_db),
):
    return get_institutions(db)


@router.get(
    "/{institution_id}",
    response_model=InstitutionRead,
)
async def get_institution_by_id_route(
    institution_id: UUID,
    db: Session = Depends(get_db),
):
    return get_institution_by_id(db, institution_id)


@router.patch(
    "/{institution_id}",
    response_model=InstitutionRead,
)
async def update_institution_route(
    institution_id: UUID,
    institution_data: InstitutionUpdate,
    db: Session = Depends(get_db),
):
    return update_institution(db, institution_id, institution_data)


@router.delete(
    "/{institution_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_institution_route(
    institution_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_institution(db, institution_id) 