"""Testing Env Setup"""

import pytest
from .test_settings import test_settings
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import create_database, database_exists
from sqlmodel import SQLModel
import logging
from fastapi.testclient import TestClient
from src.main import app
from src.database import db

logger = logging.getLogger(test_settings.ENVIRONMENT)
# Create SQLAlchemy engine
engine = create_engine(
    test_settings.SQLITE_URI,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,  # read about
)

# Creates session factory
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)


def db_setup():
    """Creates/Setups database"""
    print("runing setup")
    try:
        if not database_exists(engine.url):
            # Creates the database if it does not exist.
            logger.info("Creating database if they don't exist.")
            create_database(engine.url)
        with engine.begin() as conn:
            # Creates the tables if they don't exist.
            logger.info("Creating tables if they don't exist.")
            SQLModel.metadata.create_all(conn)
    except Exception as e:
        logger.error(e)


"""
overrides get_db()from db.py
"""


def override_get_db():
    database = TestingSessionLocal()
    try:
        yield database
    finally:
        database.close()


# injects it
app.dependency_overrides[db.get_db] = override_get_db


@pytest.fixture(scope="function")
def test_client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session", autouse=True)
def setup():
    db_setup()
    yield
