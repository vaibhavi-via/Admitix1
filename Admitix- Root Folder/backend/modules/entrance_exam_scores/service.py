from __future__ import annotations
import uuid
from fastapi import HTTPException
from sqlalchemy.orm import Session
from core.authorization import require_same_institution, require_own_student, role_name
from modules.students.models import Student
from modules.users.models import User
from .models import EntranceExamScore
from .schema import EntranceExamScoreCreate, EntranceExamScoreUpdate

def _student(db: Session, student_id: uuid.UUID, user: User) -> Student:
    student = db.get(Student, student_id)
    if student is None: raise HTTPException(status_code=404, detail="Student not found.")
    require_same_institution(user, student.institution_id); require_own_student(user, student); return student

def get_entrance_exam_score_by_id(db: Session, score_id: uuid.UUID, user: User) -> EntranceExamScore:
    item = db.get(EntranceExamScore, score_id)
    if item is None: raise HTTPException(status_code=404, detail="Entrance exam score not found.")
    _student(db, item.student_id, user); return item

def create_entrance_exam_score(db: Session, data: EntranceExamScoreCreate, user: User) -> EntranceExamScore:
    _student(db, data.student_id, user)
    item = EntranceExamScore(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item

def get_entrance_exam_scores(db: Session, student_id: uuid.UUID | None, user: User) -> list[EntranceExamScore]:
    if role_name(user) == "student": student_id = user.student_id
    query = db.query(EntranceExamScore)
    if student_id is not None: _student(db, student_id, user); query = query.filter(EntranceExamScore.student_id == student_id)
    return query.order_by(EntranceExamScore.created_at.desc()).all()

def update_entrance_exam_score(db: Session, score_id: uuid.UUID, data: EntranceExamScoreUpdate, user: User) -> EntranceExamScore:
    item = get_entrance_exam_score_by_id(db, score_id, user)
    for field, value in data.model_dump(exclude_unset=True).items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item

def delete_entrance_exam_score(db: Session, score_id: uuid.UUID, user: User) -> None:
    item = get_entrance_exam_score_by_id(db, score_id, user)
    if role_name(user) == "student": raise HTTPException(status_code=403, detail="Students cannot delete entrance exam records.")
    db.delete(item); db.commit()
