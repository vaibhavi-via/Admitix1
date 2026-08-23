from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from db.session import get_db
from core.authentication import CurrentUser

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
    upload_document_file,
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
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return create_document(db, document_data, current_user)


@router.get(
    "/",
    response_model=list[DocumentRead],
)
async def get_documents_route(
    current_user: CurrentUser,
    application_id: UUID | None = None,
    db: Session = Depends(get_db),
):
    return get_documents(db, current_user, application_id)


@router.post("/upload", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def upload_document_route(current_user: CurrentUser, application_id: UUID = Form(...), document_type_id: UUID = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await upload_document_file(db, application_id, document_type_id, file, current_user)


@router.get(
    "/{document_id}",
    response_model=DocumentRead,
)
async def get_document_by_id_route(
    document_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return get_document_by_id(db, document_id, current_user)


@router.patch(
    "/{document_id}",
    response_model=DocumentRead,
)
async def update_document_route(
    document_id: UUID,
    document_data: DocumentUpdate,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return update_document(db, document_id, document_data, current_user)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document_route(
    document_id: UUID,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return delete_document(db, document_id, current_user)
