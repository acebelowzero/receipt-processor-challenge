from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

LOGGER = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Configuration of the application"""

    # Env import
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Main
    ENVIRONMENT: Literal["development", "production", "testing"] = "development"
    
    #db
    DATABASE_URI: str = "sqlite:///app.db"

    # Logging
    LOG_CONFIG_PATH: str = "conf/logging.conf"
    LOG_FILE_PATH: str = "logs/app.log"


settings: Settings = Settings()
