from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    DepartmentCreate,
    DepartmentRead,
    DepartmentUpdate,
)
from .service import (
    create_department,
    get_departments,
    get_department_by_id,
    update_department,
    delete_department,
)

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
)


@router.post(
    "/",
    response_model=DepartmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_department_route(
    department_data: DepartmentCreate,
    db: Session = Depends(get_db),
):
    return create_department(db, department_data)


@router.get(
    "/",
    response_model=list[DepartmentRead],
)
async def get_departments_route(
    db: Session = Depends(get_db),
):
    return get_departments(db)


@router.get(
    "/{department_id}",
    response_model=DepartmentRead,
)
async def get_department_by_id_route(
    department_id: UUID,
    db: Session = Depends(get_db),
):
    return get_department_by_id(db, department_id)


@router.patch(
    "/{department_id}",
    response_model=DepartmentRead,
)
async def update_department_route(
    department_id: UUID,
    department_data: DepartmentUpdate,
    db: Session = Depends(get_db),
):
    return update_department(db, department_id, department_data)


@router.delete(
    "/{department_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_department_route(
    department_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_department(db, department_id)
