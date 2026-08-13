from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    DocumentCreate,
    DocumentRead,
    DocumentUpdate,
)
from .service import (
    create_document,
    get_documents,
    get_document_by_id,
    update_document,
    delete_document,
)

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)


@router.post(
    "/",
    response_model=DocumentRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_document_route(
    document_data: DocumentCreate,
    db: Session = Depends(get_db),
):
    return create_document(db, document_data)


@router.get(
    "/",
    response_model=list[DocumentRead],
)
async def get_documents_route(
    db: Session = Depends(get_db),
):
    return get_documents(db)


@router.get(
    "/{document_id}",
    response_model=DocumentRead,
)
async def get_document_by_id_route(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return get_document_by_id(db, document_id)


@router.patch(
    "/{document_id}",
    response_model=DocumentRead,
)
async def update_document_route(
    document_id: UUID,
    document_data: DocumentUpdate,
    db: Session = Depends(get_db),
):
    return update_document(db, document_id, document_data)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_route(
    document_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_document(db, document_id)