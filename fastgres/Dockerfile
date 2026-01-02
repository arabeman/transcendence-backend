# Official Python runtime as a parent image
FROM python:3.11-slim

WORKDIR /app

# apt-get for stability, gcc because we are using slim version
RUN apt-get update && apt-get install -y \
	gcc \
	libpq-dev \
	&& rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy only requirements to cache them in docker layer
COPY pyproject.toml poetry.lock* /app/

# Configure poetry to not create a v env'
RUN poetry config virtualenvs.create false

# Install dependencies
# Force a lock update before installing
RUN poetry lock
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code
COPY . /app

# Setup entrypoint to be executable
COPY scripts/entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# Set entrypoint
ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# Add src directory to PYTHONPATH so we can import 'heroes', 'classes', etc.
ENV PYTHONPATH="${PYTHONPATH}:/app/src"

# Default cmd to run the app
CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]

