"""This handles the link between data and business logic"""


import logging
from src.utils.config import settings
from sqlalchemy.orm import Session
from src.receipts import schema
from src.receipts import model


from .receipt_repo import receipt_repo
from .exceptions import ReceiptServiceError
from pydantic import UUID4

logger = logging.getLogger(settings.ENVIRONMENT)

class ReceiptService:
    def create_receipt(db_conn: Session, receipt: schema.Receipt):
        """
        Creates a new receipt in the database
        Args:
            db_conn (Session): database session
            receipt (Receipt): receipt data

            Raises:
                ReceiptService Exception if errors occurs

            Returns:
                UUID: Receipt ID
        """
        try:
            db_receipt = model.Receipt(
                id=receipt.id,
                retailer=receipt.retailer,
                purchaseDate=receipt.purchaseDate,
                purchaseTime=receipt.purchaseTime,
                total=receipt.total
            )
            receipt_repo.create(db_conn, db_receipt)
            logger.debug("Receipt created: %s", receipt)

            for item in receipt.items:
                db_item = model.Item(
                    receipt_id=receipt.id,
                    shortDescription=item.shortDescription,
                    price=item.price
                )
                receipt_repo.create(db_conn, db_item)
                logger.debug("Item created: %s", db_item.idx)
        except Exception as e:
            logger.exception("Error occured while creating receipt")
            raise ReceiptServiceError from e
        else:
            return receipt.id
    
    def get_receipt_by_id(db_conn: Session, receipt_id: UUID4):
        """
        Retrives receipt by id

        Args:
            db_conn (Session): database session
            receipt_id (UUID): receipt id

        Raises:
            ReceiptServiceException:
                if error occurs fetching by id
        
        Returns:
            Receipt Model
        """
        try:
            receipt = receipt_repo.get_by_id(db_conn, receipt_id)
        except Exception as e:
            raise ReceiptServiceError from e
        else:
            return receipt