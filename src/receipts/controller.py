import logging
from src.utils.config import settings
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.receipts import schema


logger = logging.getLogger(settings.ENVIRONMENT)


# receipts endpoint
router = APIRouter(prefix="/receipts")


@router.post("/process", response_model=schema.CreateReceiptResponse)
async def process_receipts(receipt:schema.Receipt):
    resp = schema.CreateReceiptResponse(**receipt.model_dump())
    return resp