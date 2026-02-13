FROM python:3.10-slim

# System dependencies
RUN apt-get update && apt-get install -y curl build-essential libpq-dev && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set PATH for Poetry
ENV PATH="/root/.local/bin:$PATH"

# Set work directory
WORKDIR /app

# Copy project files for dependency installation
COPY pyproject.toml poetry.lock* ./

# Install dependencies only (without the project itself yet)
RUN poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the code
COPY . .

# Now install the project itself (this is fast since dependencies are cached)
RUN poetry install --only-root --no-interaction --no-ansi

# Default command (can be overridden by docker-compose)
CMD ["poetry", "run", "gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8001", "--workers", "4"]
