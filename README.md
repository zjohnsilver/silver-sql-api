# Silver SQL API - Backend

FastAPI backend for Silver SQL Console - SQL query execution API.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.12
- **Validation**: Pydantic v2
- **Database Drivers**: asyncpg (PostgreSQL), aiomysql (MySQL)
- **ORM**: SQLAlchemy 2.0
- **Architecture**: Vertical Slice Architecture

## Features

- Client search and connection management
- SQL query execution with timeout and row limits
- Query validation and security checks
- Async/await throughout
- Type-safe with Pydantic models
- Vertical Slice Architecture for better feature isolation

## Getting Started

### Prerequisites

- **uv** (recommended Python package manager)
- Python 3.12+

### Installation

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Quick setup with Makefile (recommended)
make setup

# Or manually:
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .
cp .env.example .env

# Update .env with your configuration
```

### Development

```bash
# Start development server (recommended)
make start

# Or manually with uv
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or with activated venv
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Makefile Commands

The project includes a Makefile for common tasks:

- `make setup` - Setup project (create venv, install dependencies, copy .env)
- `make start` - Start development server
- `make dev` - Alias for start
- `make test` - Run tests
- `make lint` - Run linter (ruff)
- `make format` - Format code (black + ruff)
- `make clean` - Clean up generated files
- `make help` - Show all available commands

API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Production

```bash
# Run with Gunicorn + Uvicorn workers
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Endpoints

### Clients

- `GET /clients` - Search for clients
- `POST /clients/{client_id}/resolve` - Resolve client connection

### Queries

- `POST /query/execute` - Execute SQL query
- `POST /query/{query_id}/cancel` - Cancel running query

### Health

- `GET /` - API info
- `GET /health` - Health check

## Authentication

All endpoints (except `/` and `/health`) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

## Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `SECRET_KEY`: JWT signing key (change in production!)
- `DATABASE_URL`: Client management database connection
- `CORS_ORIGINS`: Allowed CORS origins
- `DEFAULT_MAX_ROWS`: Default query result limit
- `DEFAULT_TIMEOUT_SECONDS`: Default query timeout

## Project Structure (Vertical Slice Architecture)

```
app/
├── features/              # Feature slices
│   ├── clients/          # Client management feature
│   │   ├── endpoints.py  # API routes
│   │   ├── service.py    # Business logic
│   │   └── models.py     # Feature-specific models
│   └── queries/          # Query execution feature
│       ├── endpoints.py  # API routes
│       ├── service.py    # Business logic
│       └── models.py     # Feature-specific models
├── shared/               # Shared utilities and models
│   ├── config.py        # Application configuration
│   └── models.py        # Shared domain models
└── main.py              # FastAPI application
```

### Why Vertical Slice Architecture?

Each feature is self-contained with its own:
- **Endpoints**: API route handlers
- **Service**: Business logic and data access
- **Models**: Feature-specific request/response models

This approach provides:
- Better feature isolation and maintainability
- Easier to add/remove features
- Clear boundaries between features
- Reduced coupling between components

## Security Notes

- Use HTTPS in production
- Implement proper database connection pooling
- Add rate limiting for production use
- Review and enhance SQL validation rules
- Implement audit logging
- Add authentication if needed for your use case

## License

MIT

