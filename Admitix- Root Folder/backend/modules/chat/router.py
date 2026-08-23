from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db

from .schema import (
    ChatHistoryCreate,
    ChatHistoryRead,
    ChatHistoryUpdate,
)
from .service import (
    create_chat_history,
    get_chat_histories,
    get_chat_history_by_id,
    update_chat_history,
    delete_chat_history,
)

router = APIRouter(
    prefix="/chat-history",
    tags=["Chat History"],
)


@router.post(
    "/",
    response_model=ChatHistoryRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_chat_history_route(
    chat_history_data: ChatHistoryCreate,
    db: Session = Depends(get_db),
):
    return create_chat_history(db, chat_history_data)


@router.get(
    "/",
    response_model=list[ChatHistoryRead],
)
async def get_chat_histories_route(
    db: Session = Depends(get_db),
):
    return get_chat_histories(db)


@router.get(
    "/{chat_history_id}",
    response_model=ChatHistoryRead,
)
async def get_chat_history_by_id_route(
    chat_history_id: UUID,
    db: Session = Depends(get_db),
):
    return get_chat_history_by_id(db, chat_history_id)


@router.patch(
    "/{chat_history_id}",
    response_model=ChatHistoryRead,
)
async def update_chat_history_route(
    chat_history_id: UUID,
    chat_history_data: ChatHistoryUpdate,
    db: Session = Depends(get_db),
):
    return update_chat_history(db, chat_history_id, chat_history_data)


@router.delete(
    "/{chat_history_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_chat_history_route(
    chat_history_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_chat_history(db, chat_history_id)
