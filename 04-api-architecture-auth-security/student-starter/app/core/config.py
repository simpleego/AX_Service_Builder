"""환경 설정 — 이 파일은 그대로 사용하세요."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./tagtodo.db"

    SECRET_KEY: str = "tagtodo-class-secret-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    REFRESH_TOKEN_EXPIRE_DAYS: int = 14

    GOOGLE_CLIENT_ID: str = "YOUR_GOOGLE_CLIENT_ID"
    GOOGLE_CLIENT_SECRET: str = "YOUR_GOOGLE_CLIENT_SECRET"
    GOOGLE_REDIRECT_URI: str = "http://localhost:8000/auth/oauth/google/callback"

    class Config:
        env_file = ".env"


settings = Settings()
