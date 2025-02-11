from sqlmodel import SQLModel
from typing import Generic, TypeVar
from src.utils.config import settings
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from pydantic import UUID4
import logging
from .exceptions import ElementNotFoundError, DatabaseConnectionError

logger = logging.getLogger(settings.ENVIRONMENT)


T = TypeVar("SQLModel", bound=SQLModel)


class RepoBase(Generic[T]):
    """Handles CRUD
    Repository based pattern

    create
    retrieve
    update
    delete

    """

    def __init__(self, model):
        super().__init__()
        self.model = model

    def create(self, db_conn: Session, data: T):
        """
        Creates new record in the database

        Args:
            db_conn (Session): database session
            data (T): The data to be created
        """
        logger.debug("Creating object %s", self.model.__name__)
        try:
            db_conn.add(data)
            db_conn.commit()
        except OperationalError:
            db_conn.rollback()
            logger.exception("Failed to create %s object", self.model)
            raise
        else:
            return data

    def get_by_id(self, db_conn: Session, id: int | UUID4):
        logger.debug("Fetching by id: %s", id)

        data = db_conn.query(self.model).filter(self.model.id == id).first()
        if data:
            logger.debug("Found %s with ID %s", self.model.__name__, id)
            return data
        error = f"ID: {id} for model: {self.model.__name__} not found."
        logger.error(error)
        raise ElementNotFoundError(error)
