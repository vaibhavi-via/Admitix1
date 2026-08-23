from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    UserCreate,
    UserRead,
    UserUpdate,
)
from .service import (
    create_user,
    get_users,
    get_user_by_id,
    update_user,
    delete_user,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post(
    "/",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user_route(
    user_data: UserCreate,
    db: Session = Depends(get_db),
):
    return create_user(db, user_data)


@router.get(
    "/",
    response_model=list[UserRead],
)
async def get_users_route(
    db: Session = Depends(get_db),
):
    return get_users(db)


@router.get(
    "/{user_id}",
    response_model=UserRead,
)
async def get_user_by_id_route(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    return get_user_by_id(db, user_id)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
)
async def update_user_route(
    user_id: UUID,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
):
    return update_user(db, user_id, user_data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user_route(
    user_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_user(db, user_id)
