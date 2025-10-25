# Silver SQL API - Backend

FastAPI backend for Silver SQL Console - SQL query execution API.

## Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.12
- **Validation**: Pydantic v2
- **Authentication**: JWT (python-jose)
- **Database Drivers**: asyncpg (PostgreSQL), aiomysql (MySQL)
- **ORM**: SQLAlchemy 2.0

## Features

- Client search and connection management
- SQL query execution with timeout and row limits
- JWT-based authentication
- Role-based access control
- Query validation and security checks
- Async/await throughout
- Type-safe with Pydantic models

## Getting Started

### Prerequisites

- Python 3.12+
- pip or poetry

### Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env

# Update .env with your configuration
```

### Development

```bash
# Run development server with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

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

## Project Structure

```
app/
├── api/              # API route handlers
├── core/             # Core utilities (config, auth)
├── models/           # Pydantic models
├── services/         # Business logic
└── main.py           # FastAPI application
```

## Security Notes

- Change `SECRET_KEY` in production
- Use HTTPS in production
- Implement proper database connection pooling
- Add rate limiting for production use
- Review and enhance SQL validation rules
- Implement audit logging

## License

MIT

