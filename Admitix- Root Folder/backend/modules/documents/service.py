"""Business logic for the `documents` resource."""

from __future__ import annotations

import uuid

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Document
from .schema import DocumentCreate, DocumentUpdate


def create_document(db: Session, document_data: DocumentCreate) -> Document:
    """Record a newly uploaded document against an application. Starts
    in `pending` verification status by default (model server default)."""

    document = Document(**document_data.model_dump())

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(db: Session) -> list[Document]:
    """Return every document, most recently uploaded first."""

    return db.query(Document).order_by(Document.uploaded_at.desc()).all()


def get_document_by_id(db: Session, document_id: uuid.UUID) -> Document:
    """Fetch a single document by id or raise 404."""

    document = db.query(Document).filter(Document.document_id == document_id).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found."
        )

    return document


def update_document(
    db: Session, document_id: uuid.UUID, document_data: DocumentUpdate
) -> Document:
    """Partially update a document — typically a verifier setting
    `verification_status`, `verified_by`, and `remarks`."""

    document = get_document_by_id(db, document_id)

    update_data = document_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(db: Session, document_id: uuid.UUID) -> None:
    """Delete a document (cascades to its AI verification record)."""

    document = get_document_by_id(db, document_id)

    db.delete(document)
    db.commit()
