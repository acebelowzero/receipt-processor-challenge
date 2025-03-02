import logging
from src.utils.config import settings
from typing import Annotated
from fastapi import APIRouter, Depends, Path
from src.receipts import schema
from src.database import db
from sqlalchemy.orm import Session
from .service import ReceiptService
from pydantic import UUID4
from src.repo.exceptions import ElementNotFoundError
from src.exceptions import exceptions

logger = logging.getLogger(settings.ENVIRONMENT)


# receipts endpoint
router = APIRouter(prefix="/receipts")


@router.post("/process", response_model=schema.CreateReceiptResponse)
async def process_receipts(
    db_conn: Annotated[Session, Depends(db.get_db)], receipt: schema.Receipt
):
    try:
        receipt_id = ReceiptService.create_receipt(db_conn, receipt)
        return schema.CreateReceiptResponse(id=receipt_id)
    except Exception as e:
        logger.error(e)
        raise


@router.get("/{receipt_id}/points", response_model=schema.PointsResponse)
async def get_receipt_points_by_id(
    receipt_id: Annotated[UUID4, Path(description="ID of the receipt")],
    db_conn: Annotated[Session, Depends(db.get_db)],
):
    try:
        points = ReceiptService.get_points_by_id(db_conn, receipt_id)
        return points
    except ElementNotFoundError:
        raise exceptions.HTTP404NotFoundError("No receipt found for that ID.")
    except Exception as e:
        logger.error(e)
        raise
