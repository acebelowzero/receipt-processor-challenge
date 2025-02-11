"""This handles the link between data and business logic"""

import math
import logging
from src.utils.config import settings
from sqlalchemy.orm import Session
from src.receipts import schema
from src.receipts import model
from datetime import time, timedelta, datetime
from .receipt_repo import receipt_repo
from .point_repo import point_repo
from src.repo.exceptions import ElementNotFoundError
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
                total=float(receipt.total),
            )
            receipt_repo.create(db_conn, db_receipt)
            logger.debug("Receipt created: %s", receipt)

            for item in receipt.items:
                db_item = model.Item(
                    receipt_id=receipt.id,
                    shortDescription=item.shortDescription,
                    price=float(item.price),
                )
                receipt_repo.create(db_conn, db_item)
                logger.debug("Item created: %s", db_item.idx)
        except Exception as e:
            logger.error(e)
            raise exceptions.HTTP400BadRequestError from e
        try:
            points = ReceiptService._process_receipt(db_receipt)
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
            points += len(retailer)
            logger.debug(
                f"{points} points - retailer name has {len(retailer)} characters"
            )

        if helpers.check_if_whole_number(receipt.total):
            # add 50 points if total is round dollar amount
            logger.debug("Receipt Total %s is a round dollar amount", receipt.total)
            logger.debug("50 points - total is a rounded dollar")
            points += 50

        # check if receipt total is a multiple 0.25
        if helpers.check_if_whole_number(receipt.total / 0.25):
            points += 25
            logger.debug("25 points - total is a multiple of 0.25")

        # get total groups of two and multiplies by 5
        groups_of_two = helpers.count_groups_of_two(receipt.items)
        group_points = groups_of_two * 5
        points += group_points
        logger.debug(
            f"{group_points} - {len(receipt.items)} items ({groups_of_two} @ 5 points each)"
        )

        # checks if item description are multiples 3
        for item in receipt.items:
            desc = item.shortDescription.strip()
            if helpers.check_if_whole_number(len(desc) / 3):
                price_ = item.price * 0.2
                points += math.ceil(price_)
                logger.debug(
                    f"3 points - {item.shortDescription} is {len(desc)} characters (a multiple of 3), items price of {item.price} * 0.2 = {math.ceil(price_)}"
                )

        # checks if day is odd
        if helpers.is_odd(receipt.purchaseDate.day):
            points += 6
            logger.debug("6 points - purchase day is odd")

        if (
            receipt.purchaseTime > AFTER_TIME_MODIFIER
            and receipt.purchaseTime < BEFORE_TIME_MODIFIER
        ):
            points += 10
            # for logging purposes
            converted_time = helpers.convert_24_to_12_hour(receipt.purchaseTime)
            am_pm = receipt.purchaseTime.strftime("%I:%M %p")  # gets am or pm
            logger.debug(
                f"10 points - {converted_time.time()}{am_pm} is between {helpers.convert_24_to_12_hour(AFTER_TIME_MODIFIER).time()}pm and {helpers.convert_24_to_12_hour(BEFORE_TIME_MODIFIER).time()}pm"
            )
        logger.debug(f"Total points - {points}")
        return points
