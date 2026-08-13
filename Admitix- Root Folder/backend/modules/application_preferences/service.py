from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import ApplicationPreference
from .schema import ApplicationPreferenceCreate, ApplicationPreferenceUpdate
def get_application_preference_by_id(db: Session, preference_id: uuid.UUID) -> ApplicationPreference:
    item = db.query(ApplicationPreference).filter(ApplicationPreference.preference_id == preference_id).first()
    if item is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application preference not found.")
    return item
def create_application_preference(db: Session, data: ApplicationPreferenceCreate) -> ApplicationPreference:
    duplicate = db.query(ApplicationPreference).filter(ApplicationPreference.application_id == data.application_id, (ApplicationPreference.preference_no == data.preference_no) | (ApplicationPreference.course_id == data.course_id)).first()
    if duplicate: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This preference number or course already exists for the application.")
    item = ApplicationPreference(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
def get_application_preferences(db: Session, application_id: uuid.UUID | None = None) -> list[ApplicationPreference]:
    query = db.query(ApplicationPreference)
    if application_id is not None: query = query.filter(ApplicationPreference.application_id == application_id)
    return query.order_by(ApplicationPreference.application_id, ApplicationPreference.preference_no).all()
def update_application_preference(db: Session, preference_id: uuid.UUID, data: ApplicationPreferenceUpdate) -> ApplicationPreference:
    item = get_application_preference_by_id(db, preference_id)
    updates = data.model_dump(exclude_unset=True)
    if "preference_no" in updates:
        duplicate = db.query(ApplicationPreference).filter(ApplicationPreference.application_id == item.application_id, ApplicationPreference.preference_no == updates["preference_no"], ApplicationPreference.preference_id != preference_id).first()
        if duplicate: raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This preference number already exists for the application.")
    for field, value in updates.items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item
def delete_application_preference(db: Session, preference_id: uuid.UUID) -> None:
    db.delete(get_application_preference_by_id(db, preference_id)); db.commit()
