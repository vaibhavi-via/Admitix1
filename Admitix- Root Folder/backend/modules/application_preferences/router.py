from uuid import UUID
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .schema import ApplicationPreferenceCreate, ApplicationPreferenceRead, ApplicationPreferenceUpdate
from .service import create_application_preference, delete_application_preference, get_application_preference_by_id, get_application_preferences, update_application_preference
router = APIRouter(prefix="/application-preferences", tags=["Application Preferences"])
@router.post("/", response_model=ApplicationPreferenceRead, status_code=status.HTTP_201_CREATED)
def create_route(data: ApplicationPreferenceCreate, current_user: CurrentUser, db: Session = Depends(get_db)): return create_application_preference(db, data, current_user)
@router.get("/", response_model=list[ApplicationPreferenceRead])
def list_route(current_user: CurrentUser, application_id: UUID | None = Query(None), db: Session = Depends(get_db)): return get_application_preferences(db, application_id, current_user)
@router.get("/{preference_id}", response_model=ApplicationPreferenceRead)
def get_route(preference_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): return get_application_preference_by_id(db, preference_id, current_user)
@router.patch("/{preference_id}", response_model=ApplicationPreferenceRead)
def update_route(preference_id: UUID, data: ApplicationPreferenceUpdate, current_user: CurrentUser, db: Session = Depends(get_db)): return update_application_preference(db, preference_id, data, current_user)
@router.delete("/{preference_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_route(preference_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): delete_application_preference(db, preference_id, current_user)
