from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from ..core.database import get_session
from ..models.user import User
from ..schemas.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/")
def get_users(session: Session = Depends(get_session)) -> list[UserRead]:
    users = session.exec(select(User)).all()
    return [UserRead.model_validate(user) for user in users]