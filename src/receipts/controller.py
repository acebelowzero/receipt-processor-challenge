import logging
from src.utils.config import settings
from typing import Annotated
from fastapi import APIRouter, Request, Depends
from fastapi.responses import JSONResponse
from src.receipts import schema
from src.database import db
from sqlalchemy.orm import Session



logger = logging.getLogger(settings.ENVIRONMENT)


# receipts endpoint
router = APIRouter(prefix="/receipts")


@router.post("/process", response_model=schema.CreateReceiptResponse)
async def process_receipts(db_conn: Annotated[Session, Depends(db.get_db)], receipt:schema.Receipt):
    resp = schema.CreateReceiptResponse(**receipt.model_dump())
    return resp