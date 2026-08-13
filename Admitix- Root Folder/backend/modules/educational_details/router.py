from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from db.session import get_db
from .schema import EducationDetailCreate, EducationDetailRead, EducationDetailUpdate
from .service import create_education_detail, delete_education_detail, get_education_detail_by_id, get_education_details, update_education_detail
router = APIRouter(prefix="/educational-details", tags=["Educational Details"])
@router.post("/", response_model=EducationDetailRead, status_code=status.HTTP_201_CREATED)
def create_route(data: EducationDetailCreate, db: Session = Depends(get_db)): return create_education_detail(db, data)
@router.get("/", response_model=list[EducationDetailRead])
def list_route(student_id: UUID | None = Query(None), db: Session = Depends(get_db)): return get_education_details(db, student_id)
@router.get("/{education_id}", response_model=EducationDetailRead)
def get_route(education_id: UUID, db: Session = Depends(get_db)): return get_education_detail_by_id(db, education_id)
@router.patch("/{education_id}", response_model=EducationDetailRead)
def update_route(education_id: UUID, data: EducationDetailUpdate, db: Session = Depends(get_db)): return update_education_detail(db, education_id, data)
@router.delete("/{education_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(education_id: UUID, db: Session = Depends(get_db)): delete_education_detail(db, education_id)
