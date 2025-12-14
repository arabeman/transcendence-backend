from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from .models import User
from .env import DATABASE_URL, DEBUG

engine = create_engine(DATABASE_URL, echo=DEBUG)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")
    create_db_and_tables()
    yield
    print("Exiting...")

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/")
async def get_users():
    with Session(engine) as session:
        users = session.exec(select(User)).all()
        return users
