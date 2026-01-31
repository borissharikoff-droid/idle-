from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Telegram Bot
    BOT_TOKEN: str = "7568831722:AAElenff-UrkJVHQCeP8aaSEgimTDOmIZRA"
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/idlzga"
    
    # Web App
    WEBAPP_URL: str = "https://your-app.railway.app"
    API_URL: str = "https://your-api.railway.app"
    
    # Game Settings
    TICK_RATE: float = 0.1  # 100ms tick rate for smooth progress
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
