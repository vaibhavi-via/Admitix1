from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import EducationDetail
from .schema import EducationDetailCreate, EducationDetailUpdate
def get_education_detail_by_id(db: Session, education_id: uuid.UUID) -> EducationDetail:
    item = db.query(EducationDetail).filter(EducationDetail.education_id == education_id).first()
    if item is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Educational detail not found.")
    return item
def create_education_detail(db: Session, data: EducationDetailCreate) -> EducationDetail:
    item = EducationDetail(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
def get_education_details(db: Session, student_id: uuid.UUID | None = None) -> list[EducationDetail]:
    query = db.query(EducationDetail)
    if student_id is not None: query = query.filter(EducationDetail.student_id == student_id)
    return query.order_by(EducationDetail.created_at.desc()).all()
def update_education_detail(db: Session, education_id: uuid.UUID, data: EducationDetailUpdate) -> EducationDetail:
    item = get_education_detail_by_id(db, education_id)
    for field, value in data.model_dump(exclude_unset=True).items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item
def delete_education_detail(db: Session, education_id: uuid.UUID) -> None:
    db.delete(get_education_detail_by_id(db, education_id)); db.commit()
