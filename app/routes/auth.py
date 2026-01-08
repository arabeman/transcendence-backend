from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from ..core.database import get_session
from ..core.env import REFRESH_TOKEN_EXPIRE_DAYS, DEBUG
from ..schemas.auth import Token, UserCreate
from ..schemas.user import UserRead
from ..services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201)
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    try:
        user = AuthService.register_user(user_data, session)
        return UserRead.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.post("/login", response_model=Token)
def login(
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = AuthService.authenticate_user(
        form_data.username, form_data.password, session
    )
    if not user:
        raise HTTPException(status_code=401, detail="Wrong credentials")
    token = AuthService.create_access_token(user)
    refresh_token = AuthService.create_refresh_token(user)

    response.set_cookie(
        key="refreshToken",
        value=refresh_token,
        httponly=True,
        secure=not DEBUG,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,  # en seconde ito
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=Token)
def refresh_token(
    response: Response,
    refresh_token: Annotated[str | None, Cookie(alias="refreshToken")] = None,
    session: Session = Depends(get_session),
):
    user = AuthService.get_user_from_token(refresh_token, session)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    new_access_token = AuthService.create_access_token(user)
    new_refresh_token = AuthService.create_refresh_token(user)

    response.set_cookie(
        key="refreshToken",
        value=new_refresh_token,
        httponly=True,
        secure=not DEBUG,
        samesite="strict",
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
    )

    return {
        "access_token": new_access_token,
        "token_type": "bearer",
    }


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="refreshToken",
        httponly=True,
        secure=not DEBUG,
        samesite="strict",
    )
    return {"message": "Successfully logged out"}
