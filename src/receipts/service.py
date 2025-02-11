"""This handles the link between data and business logic"""

import math
import logging
from src.utils.config import settings
from sqlalchemy.orm import Session
from src.receipts import schema
from src.receipts import model
from datetime import time
from sqlite3 import IntegrityError
from .receipt_repo import receipt_repo
from .point_repo import point_repo
from src.repo.exceptions import ElementNotFoundError, DatabaseConnectionError
from .exceptions import ReceiptServiceError
from pydantic import UUID4
from src import helpers
from src.exceptions import exceptions

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
                total=receipt.total,
            )
            receipt_repo.create(db_conn, db_receipt)
            logger.debug("Receipt created: %s", receipt)

            for item in receipt.items:
                db_item = model.Item(
                    receipt_id=receipt.id,
                    shortDescription=item.shortDescription,
                    price=item.price,
                )
                receipt_repo.create(db_conn, db_item)
                logger.debug("Item created: %s", db_item.idx)
        except Exception as e:
            logger.error(e)
            raise exceptions.HTTP400BadRequestError from e
        try:
            points = ReceiptService._process_receipt(receipt)
            db_points = model.Point(id=receipt.id, points=points)
            point_repo.create(db_conn, db_points)
        except Exception as e:
            logger.exception("Error occured while creating points")
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
        except ElementNotFoundError:
            logger.error("Cannot find points with given id")
            raise
        except Exception as e:
            raise ReceiptServiceError from e
        else:
            return receipt

    def get_points_by_id(db_conn: Session, receipt_id: UUID4):
        """
        Retrives the points of a receipt
        """
        try:
            points = point_repo.get_by_id(db_conn, receipt_id)
        except ElementNotFoundError:
            logger.error("Cannot find points with given id")
            raise
        except Exception as e:
            logger.error(e)
            raise ReceiptServiceError(message=e.message)
        else:
            return points

    def _process_receipt(receipt: schema.Receipt):
        points = 0  # track points

        AFTER_TIME_MODIFIER = time(14, 0)  # After 2:00 pm
        BEFORE_TIME_MODIFIER = time(16, 0)  # Before 4:00 pm

        if receipt.retailer:
            # add one point for every alphanumeric character in the string
            retailer = helpers.remove_nonalphanumeric_characters(receipt.retailer)
            points += len(retailer) * 1

        if helpers.check_if_whole_number(receipt.total):
            # add 50 points if total is round dollar amount
            logger.debug("Receipt Total %s is a round dollar amount", receipt.total)
            points += 50

        # check if receipt total is a multiple 0.25
        if helpers.check_if_whole_number(receipt.total / 0.25):
            logger.debug("Receipt Total %s is a multiple of 0.25", receipt.total)
            points += 25

        # get total groups of two and multiplies by 5
        groups_of_two = helpers.count_groups_of_two(receipt.items)
        points += groups_of_two * 5

        # checks if item description are multiples 3
        for item in receipt.items:
            desc = item.shortDescription.strip()
            desc_ = desc.split(" ")
            if helpers.check_if_whole_number(len(desc_) / 3):
                price = math.ceil(item.price * 0.2)
                points += price

        # checks if day is odd
        if helpers.is_odd(receipt.purchaseDate.day):
            points += 5

        if (
            receipt.purchaseTime > AFTER_TIME_MODIFIER
            and receipt.purchaseTime < BEFORE_TIME_MODIFIER
        ):
            points += 10

        return points
