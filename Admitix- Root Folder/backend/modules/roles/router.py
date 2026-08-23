from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import RoleCreate, RoleRead, RoleUpdate
from .service import (
    create_role,
    get_roles,
    get_role_by_id,
    update_role,
    delete_role,
)

router = APIRouter(
    prefix="/roles",
    tags=["Roles"],
)


@router.post(
    "/",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_role_route(
    role_data: RoleCreate,
    db: Session = Depends(get_db),
):
    return create_role(db, role_data)


@router.get(
    "/",
    response_model=list[RoleRead],
)
async def get_roles_route(
    db: Session = Depends(get_db),
):
    return get_roles(db)


@router.get(
    "/{role_id}",
    response_model=RoleRead,
)
async def get_role_by_id_route(
    role_id: UUID,
    db: Session = Depends(get_db),
):
    return get_role_by_id(db, role_id)


@router.patch(
    "/{role_id}",
    response_model=RoleRead,
)
async def update_role_route(
    role_id: UUID,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
):
    return update_role(db, role_id, role_data)


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_role_route(
    role_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_role(db, role_id)
