from fastapi import FastAPI
from src.utils.config import settings
from src.utils.logging import setup_logging
from fastapi.concurrency import asynccontextmanager

# routing
from src.receipts.controller import router as receipt_router


import logging


logger = logging.getLogger(settings.ENVIRONMENT)

def on_startup():
    """Runs on server startup"""
    setup_logging()
    
    logger.info("Server is running.")
    
def on_shutdown():
    """Runs on server teardown"""
    pass
    logger.info("Server teardown")


@asynccontextmanager
async def lifespan(app: FastAPI):
    on_startup()
    yield
    on_shutdown()


app = FastAPI(lifespan=lifespan)


app.include_router(receipt_router)

