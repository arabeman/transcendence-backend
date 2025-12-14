from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_db_and_tables
from app.routes.auth import router as auth_route
from app.routes.user import router as user_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")
    create_db_and_tables()
    yield
    print("Exiting...")


app = FastAPI(lifespan=lifespan)

app.include_router(user_route)
app.include_router(auth_route)


@app.get("/")
async def root():
    return {"message": "Hello World"}
