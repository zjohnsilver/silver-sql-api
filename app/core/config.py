from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Settings
    app_name: str = "Silver SQL API"
    app_version: str = "0.1.0"
    debug: bool = False
    
    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]
    
    # JWT Settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Database Settings (Client Management DB)
    database_url: str = "postgresql://user:password@localhost/silver_sql_clients"
    
    # Query Execution Limits
    default_max_rows: int = 5000
    absolute_max_rows: int = 100000
    default_timeout_seconds: int = 30
    max_timeout_seconds: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

