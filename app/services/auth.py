from sqlmodel import Session, select

from ..models.user import User
from ..schemas.user import UserCreate


class AuthService:
    @staticmethod
    def register_user(user_data: UserCreate, session: Session) -> User:

        existing_user = session.exec(
            select(User).where(User.username == user_data.username)
        ).first()
        if existing_user:
            raise ValueError("Username already exists")

        existing_mail = session.exec(
            select(User).where(User.email == user_data.email)
        ).first()
        if existing_mail:
            raise ValueError("Email already exists")

        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=user_data.password,  #! to be hashed properly
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
