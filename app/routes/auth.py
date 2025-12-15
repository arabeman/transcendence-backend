from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..core.database import get_session
from ..schemas.user import UserCreate, UserRead
from ..services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user(user_data: UserCreate, session: Session = Depends(get_session)):
    try:
        user = AuthService.register_user(user_data, session)
        return UserRead.model_validate(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
