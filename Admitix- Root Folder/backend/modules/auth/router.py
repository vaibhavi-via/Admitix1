from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.db.session import get_db

from .schema import (
    LoginRequest,
    # LoginResponse,
    TokenResponse,
    RefreshTokenRequest,
    ChangePasswordRequest,
)

from .service import (
    login_user,
    refresh_access_token,
    logout_user,
    change_password,
    get_current_user_profile,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(db, login_data)


@router.post("/refresh-token")
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
):
    return refresh_access_token(db, refresh_data)


@router.post("/logout")
async def logout(
    db: Session = Depends(get_db),
):
    return logout_user(db)


@router.post("/change-password")
async def change_password_route(
    password_data: ChangePasswordRequest,
    db: Session = Depends(get_db),
):
    return change_password(db, password_data)


@router.get("/me")
async def get_current_user(
    db: Session = Depends(get_db),
):
    return get_current_user_profile(db)