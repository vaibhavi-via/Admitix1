from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from db.session import get_db
from core.authentication import CurrentUser
from .schema import NotificationCreate, NotificationRead, NotificationUpdate
from .service import create_notification, get_notifications, get_notification_by_id, update_notification, delete_notification
router = APIRouter(prefix="/notifications", tags=["Notifications"])
@router.post("/", response_model=NotificationRead, status_code=status.HTTP_201_CREATED)
async def create_notification_route(notification_data: NotificationCreate, current_user: CurrentUser, db: Session = Depends(get_db)): return create_notification(db, notification_data, current_user)
@router.get("/", response_model=list[NotificationRead])
async def get_notifications_route(current_user: CurrentUser, db: Session = Depends(get_db)): return get_notifications(db, current_user)
@router.get("/{notification_id}", response_model=NotificationRead)
async def get_notification_by_id_route(notification_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): return get_notification_by_id(db, notification_id, current_user)
@router.patch("/{notification_id}", response_model=NotificationRead)
async def update_notification_route(notification_id: UUID, notification_data: NotificationUpdate, current_user: CurrentUser, db: Session = Depends(get_db)): return update_notification(db, notification_id, notification_data, current_user)
@router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification_route(notification_id: UUID, current_user: CurrentUser, db: Session = Depends(get_db)): return delete_notification(db, notification_id, current_user)
