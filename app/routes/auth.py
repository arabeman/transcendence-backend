from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from ..core.database import get_session
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


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
):
    user = AuthService.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = AuthService.create_access_token(user)
    return {"access_token": token, "token_type": "bearer"}