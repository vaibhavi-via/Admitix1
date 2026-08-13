from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    DocumentTypeCreate,
    DocumentTypeRead,
    DocumentTypeUpdate,
)
from .service import (
    create_document_type,
    get_document_types,
    get_document_type_by_id,
    update_document_type,
    delete_document_type,
)

router = APIRouter(
    prefix="/document-types",
    tags=["Document Types"],
)


@router.post(
    "/",
    response_model=DocumentTypeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_type_route(
    document_type_data: DocumentTypeCreate,
    db: Session = Depends(get_db),
):
    return create_document_type(db, document_type_data)


@router.get(
    "/",
    response_model=list[DocumentTypeRead],
)
async def get_document_types_route(
    db: Session = Depends(get_db),
):
    return get_document_types(db)


@router.get(
    "/{document_type_id}",
    response_model=DocumentTypeRead,
)
async def get_document_type_by_id_route(
    document_type_id: UUID,
    db: Session = Depends(get_db),
):
    return get_document_type_by_id(db, document_type_id)


@router.patch(
    "/{document_type_id}",
    response_model=DocumentTypeRead,
)
async def update_document_type_route(
    document_type_id: UUID,
    document_type_data: DocumentTypeUpdate,
    db: Session = Depends(get_db),
):
    return update_document_type(db, document_type_id, document_type_data)


@router.delete(
    "/{document_type_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_type_route(
    document_type_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_document_type(db, document_type_id)