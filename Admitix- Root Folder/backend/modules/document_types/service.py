"""Business logic for the `document_types` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import DocumentType
from .schema import DocumentTypeCreate, DocumentTypeUpdate


def create_document_type(db: Session, document_type_data: DocumentTypeCreate) -> DocumentType:
    """Create a new document type (e.g. Aadhaar, Marksheet)."""

    document_type = DocumentType(**document_type_data.model_dump())

    db.add(document_type)
    db.commit()
    db.refresh(document_type)

    return document_type


def get_document_types(db: Session) -> list[DocumentType]:
    """Return every document type."""

    return db.query(DocumentType).order_by(DocumentType.document_name).all()


def get_document_type_by_id(db: Session, document_type_id: uuid.UUID) -> DocumentType:
    """Fetch a single document type by id or raise 404."""

    document_type = (
        db.query(DocumentType)
        .filter(DocumentType.document_type_id == document_type_id)
        .first()
    )

    if document_type is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document type not found."
        )

    return document_type


def update_document_type(
    db: Session, document_type_id: uuid.UUID, document_type_data: DocumentTypeUpdate
) -> DocumentType:
    """Partially update a document type."""

    document_type = get_document_type_by_id(db, document_type_id)

    update_data = document_type_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document_type, field, value)

    db.commit()
    db.refresh(document_type)

    return document_type


def delete_document_type(db: Session, document_type_id: uuid.UUID) -> None:
    """Delete a document type."""

    document_type = get_document_type_by_id(db, document_type_id)

    db.delete(document_type)
    db.commit()
