from fastapi import FastAPI
from src.utils.config import settings
from src.utils.logging import setup_logging
from fastapi.concurrency import asynccontextmanager
from src.database import db
from src.exceptions import exception_handlers

# routing
from src.receipts.controller import router as receipt_router


import logging


logger = logging.getLogger(settings.ENVIRONMENT)


def on_startup():
    """Runs on server startup"""
    setup_logging()
    db.db_setup()

    logger.info("Server is running.")


def on_shutdown():
    """Runs on server teardown"""
    logger.info("Server teardown")
    pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()

    yield
    on_shutdown()


app = FastAPI(lifespan=lifespan)

# setup exception handler
exception_handlers.setup_api_exceptions(app)

app.include_router(receipt_router)
