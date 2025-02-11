from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.pool import StaticPool


class TestSettings(BaseSettings):
    SQLITE_URI: str = "sqlite:///testing.db"
    ENVIRONMENT: str = "testing"


test_settings: TestSettings = TestSettings()
