from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, require_own_student, role_name
from modules.applications.models import Application
from modules.students.models import Student
from modules.users.models import User
from .models import ApplicationPreference
from .schema import ApplicationPreferenceCreate, ApplicationPreferenceUpdate

def _application(db: Session, application_id: uuid.UUID, user: User) -> Application:
    item = db.get(Application, application_id)
    if item is None: raise HTTPException(status_code=404, detail="Application not found.")
    student = db.get(Student, item.student_id)
    require_same_institution(user, student.institution_id); require_own_student(user, student)
    return item

def get_application_preference_by_id(db: Session, preference_id: uuid.UUID, user: User) -> ApplicationPreference:
    item = db.get(ApplicationPreference, preference_id)
    if item is None: raise HTTPException(status_code=404, detail="Application preference not found.")
    _application(db, item.application_id, user); return item

def create_application_preference(db: Session, data: ApplicationPreferenceCreate, user: User) -> ApplicationPreference:
    _application(db, data.application_id, user)
    duplicate = db.query(ApplicationPreference).filter(ApplicationPreference.application_id == data.application_id, (ApplicationPreference.preference_no == data.preference_no) | (ApplicationPreference.course_id == data.course_id)).first()
    if duplicate: raise HTTPException(status_code=409, detail="This preference number or course already exists for the application.")
    item = ApplicationPreference(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

def get_application_preferences(db: Session, application_id: uuid.UUID | None, user: User) -> list[ApplicationPreference]:
    query = db.query(ApplicationPreference)
    if application_id is not None:
        _application(db, application_id, user); query = query.filter(ApplicationPreference.application_id == application_id)
    elif role_name(user) == "student":
        ids = [a.application_id for a in db.query(Application).join(Student).filter(Student.user_id == user.user_id).all()]
        query = query.filter(ApplicationPreference.application_id.in_(ids or [uuid.uuid4()]))
    return query.order_by(ApplicationPreference.application_id, ApplicationPreference.preference_no).all()

def update_application_preference(db: Session, preference_id: uuid.UUID, data: ApplicationPreferenceUpdate, user: User) -> ApplicationPreference:
    item = get_application_preference_by_id(db, preference_id, user)
    updates = data.model_dump(exclude_unset=True)
    if "preference_no" in updates:
        duplicate = db.query(ApplicationPreference).filter(ApplicationPreference.application_id == item.application_id, ApplicationPreference.preference_no == updates["preference_no"], ApplicationPreference.preference_id != preference_id).first()
        if duplicate: raise HTTPException(status_code=409, detail="This preference number already exists for the application.")
    for field, value in updates.items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item

def delete_application_preference(db: Session, preference_id: uuid.UUID, user: User) -> None:
    item = get_application_preference_by_id(db, preference_id, user)
    if role_name(user) == "student": raise HTTPException(status_code=403, detail="Students cannot delete application preferences.")
    db.delete(item); db.commit()
