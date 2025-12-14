# transcendence-backend

Backend API built with FastAPI and SQLModel.

## Setup
```
poetry install
```

Create a `.env` file:
```
DATABASE_URL=sqlite:///./data/database.db
DEBUG=true
```

## Run (dev)
```
poetry run poe dev
```

API: `http://127.0.0.1:8000/`
API docs: `http://127.0.0.1:8000/docs`