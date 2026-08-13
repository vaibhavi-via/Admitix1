from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from db.session import get_db
from .schema import EntranceExamScoreCreate, EntranceExamScoreRead, EntranceExamScoreUpdate
from .service import create_entrance_exam_score, delete_entrance_exam_score, get_entrance_exam_score_by_id, get_entrance_exam_scores, update_entrance_exam_score
router = APIRouter(prefix="/entrance-exam-scores", tags=["Entrance Exam Scores"])
@router.post("/", response_model=EntranceExamScoreRead, status_code=status.HTTP_201_CREATED)
def create_route(data: EntranceExamScoreCreate, db: Session = Depends(get_db)): return create_entrance_exam_score(db, data)
@router.get("/", response_model=list[EntranceExamScoreRead])
def list_route(student_id: UUID | None = Query(None), db: Session = Depends(get_db)): return get_entrance_exam_scores(db, student_id)
@router.get("/{score_id}", response_model=EntranceExamScoreRead)
def get_route(score_id: UUID, db: Session = Depends(get_db)): return get_entrance_exam_score_by_id(db, score_id)
@router.patch("/{score_id}", response_model=EntranceExamScoreRead)
def update_route(score_id: UUID, data: EntranceExamScoreUpdate, db: Session = Depends(get_db)): return update_entrance_exam_score(db, score_id, data)
@router.delete("/{score_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(score_id: UUID, db: Session = Depends(get_db)): delete_entrance_exam_score(db, score_id)
