from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI App"
    app_env: str = "development"
    app_version: str = "1.0.0"

    # Database connection (prefer DATABASE_URL, fall back to MySQL pieces, otherwise local SQLite)
    database_url: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_user: str | None = None
    db_password: str | None = None
    db_name: str | None = None
    sqlalchemy_echo: bool = False

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

    def sqlalchemy_database_url(self) -> str:
        if self.database_url:
            return self.database_url
        if all(
            value is not None
            for value in (self.db_user, self.db_password, self.db_host, self.db_port, self.db_name)
        ):
            return (
                f"mysql+pymysql://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        return "sqlite:///./app.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
