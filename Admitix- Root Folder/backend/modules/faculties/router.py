from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    FacultyCreate,
    FacultyRead,
    FacultyUpdate,
)
from .service import (
    create_faculty,
    get_faculties,
    get_faculty_by_id,
    update_faculty,
    delete_faculty,
)

router = APIRouter(
    prefix="/faculties",
    tags=["Faculties"],
)


@router.post(
    "/",
    response_model=FacultyRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_faculty_route(
    faculty_data: FacultyCreate,
    db: Session = Depends(get_db),
):
    return create_faculty(db, faculty_data)


@router.get(
    "/",
    response_model=list[FacultyRead],
)
async def get_faculties_route(
    db: Session = Depends(get_db),
):
    return get_faculties(db)


@router.get(
    "/{faculty_id}",
    response_model=FacultyRead,
)
async def get_faculty_by_id_route(
    faculty_id: UUID,
    db: Session = Depends(get_db),
):
    return get_faculty_by_id(db, faculty_id)


@router.patch(
    "/{faculty_id}",
    response_model=FacultyRead,
)
async def update_faculty_route(
    faculty_id: UUID,
    faculty_data: FacultyUpdate,
    db: Session = Depends(get_db),
):
    return update_faculty(db, faculty_id, faculty_data)


@router.delete(
    "/{faculty_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_faculty_route(
    faculty_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_faculty(db, faculty_id) 
