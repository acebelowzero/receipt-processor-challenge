import logging
from src.utils.config import settings
from typing import Annotated
from fastapi import APIRouter, Request, Depends, Path
from fastapi.responses import JSONResponse
from src.receipts import schema
from src.receipts import model
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
    # resp = schema.CreateReceiptResponse(**receipt.model_dump())
    print(receipt)
    try:
        receipt_id = ReceiptService.create_receipt(db_conn, receipt)
        return schema.CreateReceiptResponse(id=receipt_id)
    except Exception as e:
        pass


@router.get("/{receipt_id}", response_model=schema.Receipt)
async def get_receipt_by_id(
    receipt_id: Annotated[UUID4, Path(description="ID of the receipt")],
    db_conn: Annotated[Session, Depends(db.get_db)],
):
    try:
        receipt_id = ReceiptService.get_receipt_by_id(db_conn, receipt_id)
        return receipt_id
    except Exception as e:
        pass


@router.get("/{receipt_id}/points", response_model=schema.PointsResponse)
async def get_receipt_points_by_id(
    receipt_id: Annotated[UUID4, Path(description="ID of the receipt")],
    db_conn: Annotated[Session, Depends(db.get_db)],
):
    try:
        points = ReceiptService.get_points_by_id(db_conn, receipt_id)
        return points
    except ElementNotFoundError as e:
        raise exceptions.HTTP404NotFoundError from e
