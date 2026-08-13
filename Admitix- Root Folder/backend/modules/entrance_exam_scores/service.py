from __future__ import annotations
import uuid
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from .models import EntranceExamScore
from .schema import EntranceExamScoreCreate, EntranceExamScoreUpdate
def get_entrance_exam_score_by_id(db: Session, score_id: uuid.UUID) -> EntranceExamScore:
    item = db.query(EntranceExamScore).filter(EntranceExamScore.score_id == score_id).first()
    if item is None: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Entrance exam score not found.")
    return item
def create_entrance_exam_score(db: Session, data: EntranceExamScoreCreate) -> EntranceExamScore:
    item = EntranceExamScore(**data.model_dump()); db.add(item); db.commit(); db.refresh(item); return item
def get_entrance_exam_scores(db: Session, student_id: uuid.UUID | None = None) -> list[EntranceExamScore]:
    query = db.query(EntranceExamScore)
    if student_id is not None: query = query.filter(EntranceExamScore.student_id == student_id)
    return query.order_by(EntranceExamScore.created_at.desc()).all()
def update_entrance_exam_score(db: Session, score_id: uuid.UUID, data: EntranceExamScoreUpdate) -> EntranceExamScore:
    item = get_entrance_exam_score_by_id(db, score_id)
    for field, value in data.model_dump(exclude_unset=True).items(): setattr(item, field, value)
    db.commit(); db.refresh(item); return item
def delete_entrance_exam_score(db: Session, score_id: uuid.UUID) -> None:
    db.delete(get_entrance_exam_score_by_id(db, score_id)); db.commit()
