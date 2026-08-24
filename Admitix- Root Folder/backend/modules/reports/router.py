from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .service import generate_admission_report, generate_payment_report, generate_document_report, generate_student_report, export_report
router = APIRouter(prefix="/reports", tags=["Reports"])
@router.get("/admissions")
async def admission_report(current_user: CurrentUser, db: Session = Depends(get_db)): return generate_admission_report(db, current_user)
@router.get("/payments")
async def payment_report(current_user: CurrentUser, db: Session = Depends(get_db)): return generate_payment_report(db, current_user)
@router.get("/documents")
async def document_report(current_user: CurrentUser, db: Session = Depends(get_db)): return generate_document_report(db, current_user)
@router.get("/students")
async def student_report(current_user: CurrentUser, db: Session = Depends(get_db)): return generate_student_report(db, current_user)
@router.get("/export")
async def export_report_route(current_user: CurrentUser, db: Session = Depends(get_db)): return export_report(db, current_user)
