from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..core.database import get_session
from ..models import User

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users
