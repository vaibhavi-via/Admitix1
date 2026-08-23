from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

from .service import (
    generate_admission_report,
    generate_payment_report,
    generate_document_report,
    generate_student_report,
    export_report,
)

router = APIRouter(
    prefix="/reports",
    tags=["Reports"],
)


@router.get("/admissions")
async def admission_report(
    db: Session = Depends(get_db),
):
    return generate_admission_report(db)


@router.get("/payments")
async def payment_report(
    db: Session = Depends(get_db),
):
    return generate_payment_report(db)


@router.get("/documents")
async def document_report(
    db: Session = Depends(get_db),
):
    return generate_document_report(db)


@router.get("/students")
async def student_report(
    db: Session = Depends(get_db),
):
    return generate_student_report(db)


@router.get("/export")
async def export_report_route(
    db: Session = Depends(get_db),
):
    return export_report(db)
