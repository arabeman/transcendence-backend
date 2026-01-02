import os
from sqlmodel import SQLModel, create_engine
import models

def load_password() -> str:
    pw_file = os.getenv("POSTGRES_PASSWORD_FILE") # POSTGRES_PASSWORD_FILE:  the getenv value ==> /run/secrets/postgres_password
    if pw_file and os.path.exists(pw_file):
        with open(pw_file) as f: # garantees the file is closed immediately after read
            return f.read().strip()
    return os.getenv("POSTGRES_PASSWORD", "postgres") # postgres is a fallback value

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_NAME = os.getenv("POSTGRES_DB", "game_db")
DB_HOST = os.getenv("POSTGRES_HOST", "db") # USE LOCALHOST if running outside docker
DB_PORT = os.getenv("POSTGRES_PORT", "5432")

# 1. Define connection string
# Note the 'postgresql+psycopg' scheme
DATABASE_URL = f"postgresql+psycopg://{DB_USER}:{load_password()}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. Create the engine (the connection manager)
engine = create_engine(DATABASE_URL, echo=False)

# 3. Function to create tables
def create_db_and_tables() -> None:
    # This looks at all SQLModel classes imported and creates tables for them
    SQLModel.metadata.create_all(engine)