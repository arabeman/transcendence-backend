# transcendence-backend

Backend API built with FastAPI and SQLModel.

## Prerequisites

Before setting up the project, you'll need to install:

### Poetry - Dependency Management Tool

Poetry is a tool for dependency management and packaging in Python.

**Installation:**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

**Verify installation:**
```bash
poetry --version
```

**Optional - Enable bash completions:**
```bash
poetry completions bash >> ~/.bash_completion
```

For other shells or installation methods, visit: https://python-poetry.org/docs/#installation

---

### Poe the Poet - Task Runner

Poe the Poet is a task runner that works well with Poetry projects.

**Installation:**

Add poethepoet as a dev dependency to your project:
```bash
poetry add --group dev poethepoet
```

**Verify installation:**
```bash
poetry run poe
```

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