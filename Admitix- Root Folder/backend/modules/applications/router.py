from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    ApplicationCreate,
    ApplicationRead,
    ApplicationUpdate,
)
from .service import (
    create_application,
    get_applications,
    get_application_by_id,
    update_application,
    delete_application,
)

router = APIRouter(
    prefix="/applications",
    tags=["Applications"],
)


@router.post(
    "/",
    response_model=ApplicationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_application_route(
    application_data: ApplicationCreate,
    db: Session = Depends(get_db),
):
    return create_application(db, application_data)


@router.get(
    "/",
    response_model=list[ApplicationRead],
)
async def get_applications_route(
    db: Session = Depends(get_db),
):
    return get_applications(db)


@router.get(
    "/{application_id}",
    response_model=ApplicationRead,
)
async def get_application_by_id_route(
    application_id: UUID,
    db: Session = Depends(get_db),
):
    return get_application_by_id(db, application_id)


@router.patch(
    "/{application_id}",
    response_model=ApplicationRead,
)
async def update_application_route(
    application_id: UUID,
    application_data: ApplicationUpdate,
    db: Session = Depends(get_db),
):
    return update_application(db, application_id, application_data)


@router.delete(
    "/{application_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_application_route(
    application_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_application(db, application_id)