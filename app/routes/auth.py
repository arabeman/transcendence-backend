from fastapi import APIRouter, Depends
from sqlmodel import Session

from ..core.database import get_session
from ..models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register_user(user: User, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
