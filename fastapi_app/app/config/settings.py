from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App
    app_name: str = "FastAPI App"
    app_env: str = "development"
    app_version: str = "1.0.0"

    # Database
    db_host: str
    db_port: int
    db_user: str 
    db_password: str
    db_name: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8"
    }

settings = Settings()