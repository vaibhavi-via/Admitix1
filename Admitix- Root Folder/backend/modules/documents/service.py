"""Business logic for the `documents` resource."""

from __future__ import annotations

import uuid
import re
from pathlib import Path
from fastapi import UploadFile

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from .models import Document
from .schema import DocumentCreate, DocumentUpdate
from core.authorization import require_same_institution, role_name
from modules.applications.models import Application
from modules.students.models import Student
from modules.users.models import User


def create_document(db: Session, document_data: DocumentCreate, current_user: User) -> Document:
    """Record a newly uploaded document against an application. Starts
    in `pending` verification status by default (model server default)."""

    application = db.get(Application, document_data.application_id)
    if application is None: raise HTTPException(status_code=404, detail="Application not found.")
    student = db.get(Student, application.student_id)
    require_same_institution(current_user, student.institution_id)
    if role_name(current_user) == "student" and student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You can only upload your own documents.")
    document = Document(**document_data.model_dump())

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


def get_documents(db: Session, current_user: User, application_id: uuid.UUID | None = None) -> list[Document]:
    """Return every document, most recently uploaded first."""

    query = db.query(Document).join(Application, Document.application_id == Application.application_id).join(Student, Application.student_id == Student.student_id)
    if current_user.institution_id is not None: query = query.filter(Student.institution_id == current_user.institution_id)
    if role_name(current_user) == "student": query = query.filter(Student.user_id == current_user.user_id)
    if application_id: query = query.filter(Document.application_id == application_id)
    return query.order_by(Document.uploaded_at.desc()).all()


def get_document_by_id(db: Session, document_id: uuid.UUID, current_user: User) -> Document:
    """Fetch a single document by id or raise 404."""

    document = db.query(Document).filter(Document.document_id == document_id).first()

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Document not found."
        )

    student = db.query(Student).join(Application, Application.student_id == Student.student_id).filter(Application.application_id == document.application_id).first()
    require_same_institution(current_user, student.institution_id)
    if role_name(current_user) == "student" and student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You cannot access this document.")
    return document


def update_document(
    db: Session, document_id: uuid.UUID, document_data: DocumentUpdate, current_user: User
) -> Document:
    """Partially update a document — typically a verifier setting
    `verification_status`, `verified_by`, and `remarks`."""

    document = get_document_by_id(db, document_id, current_user)

    update_data = document_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document, field, value)

    db.commit()
    db.refresh(document)

    return document


def delete_document(db: Session, document_id: uuid.UUID, current_user: User) -> None:
    """Delete a document (cascades to its AI verification record)."""

    document = get_document_by_id(db, document_id, current_user)

    db.delete(document)
    db.commit()


async def upload_document_file(db: Session, application_id: uuid.UUID, document_type_id: uuid.UUID, upload: UploadFile, current_user: User) -> Document:
    application = db.get(Application, application_id)
    if application is None: raise HTTPException(status_code=404, detail="Application not found.")
    student = db.get(Student, application.student_id)
    require_same_institution(current_user, student.institution_id)
    if role_name(current_user) == "student" and student.user_id != current_user.user_id: raise HTTPException(status_code=403, detail="You can only upload your own documents.")
    if (upload.content_type or '').lower() not in {'application/pdf','image/jpeg','image/jpg','image/png','image/webp'}: raise HTTPException(status_code=400, detail="Only PDF, JPG, PNG or WEBP files are allowed.")
    raw = await upload.read()
    if not raw or len(raw) > 12*1024*1024: raise HTTPException(status_code=400, detail="File must be smaller than 12 MB.")
    safe = re.sub(r'[^A-Za-z0-9._-]+','_',upload.filename or 'document')
    base = Path(__file__).resolve().parents[2] / 'uploads' / str(student.institution_id) / str(application_id); base.mkdir(parents=True, exist_ok=True)
    stored = f'{uuid.uuid4().hex}_{safe}'; (base/stored).write_bytes(raw)
    doc = Document(application_id=application_id, document_type_id=document_type_id, file_name=upload.filename or safe, file_url=f'/uploads/{student.institution_id}/{application_id}/{stored}')
    db.add(doc); db.commit(); db.refresh(doc); return doc
