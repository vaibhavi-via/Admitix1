from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .schema import ApplicationStatusHistoryRead
from .service import get_application_status_history, get_application_status_history_by_id

router = APIRouter(prefix="/application-status-history", tags=["Application Status History"])

@router.get("/", response_model=list[ApplicationStatusHistoryRead])
async def list_status_history(current_user: CurrentUser, db: Session = Depends(get_db)):
    return get_application_status_history(db, current_user)

@router.get("/{history_id}", response_model=ApplicationStatusHistoryRead)
async def get_status_history(history_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)):
    return get_application_status_history_by_id(db, history_id, current_user)
