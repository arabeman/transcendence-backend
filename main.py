from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session, select
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
from models import User

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG = os.getenv("DEBUG") == "True"
engine = create_engine(DATABASE_URL, echo=DEBUG)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting...")
    create_db_and_tables()
    create_user()
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

def create_user():
    user = User(id=42, email="test@gmail.com", username="test")
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user