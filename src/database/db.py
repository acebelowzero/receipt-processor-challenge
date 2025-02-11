import logging
from typing import Iterator
from sqlmodel import SQLModel

from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy_utils import create_database, database_exists
from sqlalchemy.exc import OperationalError
from src.utils.config import settings

logger = logging.getLogger(settings.ENVIRONMENT)


engine = create_engine(settings.DATABASE_URI)

localSession = sessionmaker(autoflush=False, bind=engine)

def db_setup():
    """Creates/Setups the database"""
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


# Dependency to get database session
def get_db() -> Iterator[Session]:
    """
    Gets a database session

    Create generator for a database session
    and closes it when done
    """
    database = localSession()
    try: 
        yield database
    except OperationalError as e:
        # raise HTTPServiceError()
        raise Exception(e)
    finally:
        database.close()
