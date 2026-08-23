from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import DomainCreate, DomainRead, DomainUpdate
from .service import (
    create_domain,
    get_domains,
    get_domain_by_id,
    update_domain,
    delete_domain,
)

router = APIRouter(
    prefix="/domains",
    tags=["Domains"],
)


@router.post(
    "/",
    response_model=DomainRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_domain_route(
    domain_data: DomainCreate,
    db: Session = Depends(get_db),
):
    return create_domain(db, domain_data)


@router.get(
    "/",
    response_model=list[DomainRead],
)
async def get_domains_route(
    db: Session = Depends(get_db),
):
    return get_domains(db)


@router.get(
    "/{domain_id}",
    response_model=DomainRead,
)
async def get_domain_by_id_route(
    domain_id: UUID,
    db: Session = Depends(get_db),
):
    return get_domain_by_id(db, domain_id)


@router.patch(
    "/{domain_id}",
    response_model=DomainRead,
)
async def update_domain_route(
    domain_id: UUID,
    domain_data: DomainUpdate,
    db: Session = Depends(get_db),
):
    return update_domain(db, domain_id, domain_data)


@router.delete(
    "/{domain_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_domain_route(
    domain_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_domain(db, domain_id)
