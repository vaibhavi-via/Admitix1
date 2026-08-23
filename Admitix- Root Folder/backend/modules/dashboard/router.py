from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from db.session import get_db

from .service import (
    get_dashboard_summary,
    get_admission_statistics,
    get_recent_applications,
    get_payment_summary,
    get_document_statistics,
)

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get("/summary")
async def get_dashboard_summary_route(
    db: Session = Depends(get_db),
):
    return get_dashboard_summary(db)


@router.get("/admission-statistics")
async def get_admission_statistics_route(
    db: Session = Depends(get_db),
):
    return get_admission_statistics(db)


@router.get("/recent-applications")
async def get_recent_applications_route(
    db: Session = Depends(get_db),
):
    return get_recent_applications(db)


@router.get("/payment-summary")
async def get_payment_summary_route(
    db: Session = Depends(get_db),
):
    return get_payment_summary(db)


@router.get("/document-statistics")
async def get_document_statistics_route(
    db: Session = Depends(get_db),
):
    return get_document_statistics(db)
