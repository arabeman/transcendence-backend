from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlmodel import Session, select

from app.schemas.user import UserRead
from ..core.database import get_session
from ..core.env import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    ALGORITHM,
    SECRET_KEY,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from ..core.security import hash_password, verify_password
from ..models.user import User
from ..schemas.auth import UserCreate

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


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
            raise ValueError("Email already in use")

        # TODO: fullname handling
        new_user = User(
            email=user_data.email,
            username=user_data.username,
            hashed_password=hash_password(user_data.password),
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

    @staticmethod
    def authenticate_user(username: str, password: str, session: Session):
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_access_token(user: User):
        encode = {"sub": user.username, "id": user.id}
        expires = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        encode.update({"exp": expires})
        token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def create_refresh_token(user: User):
        encode = {"sub": user.username, "id": user.id}
        expires = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        encode.update({"exp": expires})
        token = jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def get_user_from_token(token: str, session: Session):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            id: int = payload.get("id")
            if None in [username, id]:
                return None
            user = session.exec(select(User).where(User.id == id)).first()
            return user
        except JWTError:
            return None

    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme),
        session: Session = Depends(get_session),
    ):
        try:
            user = AuthService.get_user_from_token(token, session)
            if user is None:
                raise HTTPException(status_code=401, detail="Wrong credentials")
            return UserRead.model_validate(user)
        except JWTError:
            raise HTTPException(status_code=401, detail="Wrong credentials")
