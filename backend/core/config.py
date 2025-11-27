import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Application Server
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000
    
    # Filesystem Paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR: str = os.path.join(BASE_DIR, "..", "local_data")
    
    # Frontend Entry Point
    FRONTEND_DIR: str = os.path.join(BASE_DIR, "..", "frontend")
    STARTUP_URL: str = f"http://{APP_HOST}:{APP_PORT}"

    # Nuova sintassi Pydantic V2
    model_config = SettingsConfigDict(env_file=".env")

# Create a singleton instance
settings = Settings()

# Ensure data directory exists
os.makedirs(settings.DATA_DIR, exist_ok=True)