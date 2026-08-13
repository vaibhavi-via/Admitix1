from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    AIVerificationCreate,
    AIVerificationRead,
    AIVerificationUpdate,
)
from .service import (
    create_ai_verification,
    get_ai_verifications,
    get_ai_verification_by_id,
    update_ai_verification,
    delete_ai_verification,
)

router = APIRouter(
    prefix="/ai-verifications",
    tags=["AI Verification"],
)


@router.post(
    "/",
    response_model=AIVerificationRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_ai_verification_route(
    ai_verification_data: AIVerificationCreate,
    db: Session = Depends(get_db),
):
    return create_ai_verification(db, ai_verification_data)


@router.get(
    "/",
    response_model=list[AIVerificationRead],
)
async def get_ai_verifications_route(
    db: Session = Depends(get_db),
):
    return get_ai_verifications(db)


@router.get(
    "/{verification_id}",
    response_model=AIVerificationRead,
)
async def get_ai_verification_by_id_route(
    verification_id: UUID,
    db: Session = Depends(get_db),
):
    return get_ai_verification_by_id(db, verification_id)


@router.patch(
    "/{verification_id}",
    response_model=AIVerificationRead,
)
async def update_ai_verification_route(
    verification_id: UUID,
    ai_verification_data: AIVerificationUpdate,
    db: Session = Depends(get_db),
):
    return update_ai_verification(
        db,
        verification_id,
        ai_verification_data,
    )


@router.delete(
    "/{verification_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ai_verification_route(
    verification_id: UUID,
    db: Session = Depends(get_db),
):
    return delete_ai_verification(db, verification_id) 