from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.core.database import create_db_and_tables, get_session
from app.models.user import User
from app.routes.auth import router as auth_route
from app.routes.user import router as user_route
from app.services.auth import AuthService


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")
    create_db_and_tables()
    yield
    print("Exiting...")

app = FastAPI(lifespan=lifespan)

app.include_router(user_route)
app.include_router(auth_route)

db_dependency = Annotated[Session, Depends(get_session)]
user_dependency = Annotated[User, Depends(AuthService.get_current_user)]

# to test login
@app.get("/", status_code=200)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authentication Failed")
    return {"User": user}