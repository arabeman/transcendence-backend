# transcendence-backend

Backend API built with FastAPI and SQLModel.

## Prerequisites

Before setting up the project, you'll need to install:

- **Poetry** - Dependency management tool
  - Install: https://python-poetry.org/docs/#installation
- **Poe the Poet** - Task runner
  - Install: https://poethepoet.natn.io/installation.html

## Setup

```bash
poetry install
```

Create a `.env` file based on `.env.example`:

```shellscript
SECRET_KEY="hehe"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL="sqlite:///./data/database.db"
DEBUG=true
```

## Run (dev)

```bash
poetry run poe dev
```

- API: `http://127.0.0.1:8000/`
- API docs: `http://127.0.0.1:8000/docs`