from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_NAME: str = "Silver SQL API"
    API_VERSION: str = "0.1.0"
    DEBUG: bool = False

    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    DATABASE_URL: str = (
        "postgresql://user:password@localhost/silver_sql_clients"
    )

    DEFAULT_MAX_ROWS: int = 5000
    ABSOLUTE_MAX_ROWS: int = 100000
    DEFAULT_TIMEOUT_SECONDS: int = 30
    MAX_TIMEOUT_SECONDS: int = 300

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
