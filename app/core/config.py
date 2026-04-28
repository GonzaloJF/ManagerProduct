from urllib.parse import quote_plus

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    PROJECT_NAME: str = "Manager Products API"
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

    # DB: full URL or USER + PASSWORD (legacy) for postgresql://USER:PASS@localhost:5432/gestor_db
    DATABASE_URL: str | None = None
    USER: str | None = Field(default=None, description="Postgres user (legacy .env key)")
    PASSWORD: str | None = Field(default=None, description="Postgres password (legacy .env key)")

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    def sqlalchemy_database_url(self) -> str:
        if self.DATABASE_URL:
            return self.DATABASE_URL
        if not self.USER or self.PASSWORD is None:
            raise ValueError(
                "Configure DATABASE_URL or both USER and PASSWORD in .env for the database connection."
            )
        encoded_password = quote_plus(self.PASSWORD)
        return f"postgresql://{self.USER}:{encoded_password}@localhost:5432/gestor_db"


settings = Settings()
