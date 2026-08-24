from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .schema import StudentCreate, StudentRead, StudentUpdate
from .service import create_student, get_students, get_student_by_id, update_student, delete_student

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student_route(student_data: StudentCreate, current_user: CurrentUser, db: Session = Depends(get_db)):
    return create_student(db, student_data, current_user)

@router.get("/", response_model=list[StudentRead])
async def get_students_route(current_user: CurrentUser, db: Session = Depends(get_db)):
    return get_students(db, current_user)

@router.get("/{student_id}", response_model=StudentRead)
async def get_student_by_id_route(student_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)):
    return get_student_by_id(db, student_id, current_user)

@router.patch("/{student_id}", response_model=StudentRead)
async def update_student_route(student_id: UUID, student_data: StudentUpdate, current_user: CurrentUser, db: Session = Depends(get_db)):
    return update_student(db, student_id, student_data, current_user)

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student_route(student_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)):
    return delete_student(db, student_id, current_user)
