# No Pain - Doctor Working Hours Tracker

## Setup

### 1. Clone and Install Dependencies
```shell
git clone <repository-url>
cd no_pain
poetry install
```

### 2. Configure Environment
```shell
# Copy the example environment file
cp .env.example .env

# Edit .env with your settings
# For local development, keep USE_SQLITE=true
# For production, set USE_SQLITE=false
```

## Running Locally

### Option 1: Using Just (Recommended)
```shell
# Start local development server with SQLite
just start_local
```

### Option 2: Manual
```shell
# Make sure USE_SQLITE=true in your .env file
poetry run uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

The application will be available at `http://localhost:8001`

## Running in Production (Docker)

### On Raspberry Pi or Production Server:

1. **Update `.env` file:**
   ```shell
   # Set USE_SQLITE=false (or remove the line)
   # Make sure POSTGRES_SERVER=db
   USE_SQLITE=false
   POSTGRES_SERVER=db
   ```

2. **Deploy:**
   ```shell
   # Pull latest changes
   git pull

   # Rebuild and start containers
   sudo docker-compose down
   sudo docker-compose build --no-cache
   sudo docker-compose up -d

   # Check logs
   sudo docker-compose logs -f
   ```

## Database Configuration

This application supports dual database modes:

- **SQLite** (Local Development): Set `USE_SQLITE=true` in `.env`
  - No additional setup required
  - Database file: `./sql_app.db`
  
- **PostgreSQL** (Production): Set `USE_SQLITE=false` in `.env`
  - Automatically configured via docker-compose
  - Database runs in a separate container
  - Data persists in Docker volume

## Tests

To run tests:
```shell
poetry run pytest no_pain/backend/tests
```

## Project Structure

- `no_pain/backend/` - Backend application code
- `no_pain/backend/db/` - Database models and session management
- `no_pain/backend/routes/` - API routes
- `docker-compose.yml` - Production deployment configuration
- `Dockerfile` - Container build configuration

