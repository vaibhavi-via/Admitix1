from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from db.session import get_db
from core.authentication import CurrentUser

from .schema import (
    LoginRequest,
    RegisterRequest,
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
    register_student,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return register_student(db, data)


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
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return logout_user(db, current_user.user_id)


@router.post("/change-password")
async def change_password_route(
    password_data: ChangePasswordRequest,
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return change_password(db, password_data, current_user.user_id)


@router.get("/me")
async def get_current_user(
    current_user: CurrentUser,
    db: Session = Depends(get_db),
):
    return get_current_user_profile(db, current_user.user_id)
