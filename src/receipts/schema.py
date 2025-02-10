from pydantic import BaseModel, Field, UUID4
from datetime import date, time
from typing import List
import uuid
class Items(BaseModel):
    """Item schema

    Attributes:
        shortDescription (str): description of
            the item

        price (float): price of the item
    
    """
    shortDescription: str = Field()
    price: float = Field()


class Receipt(BaseModel):
    """
    Receipt Schema
    Attributes:
        id (uuid4): id of the receipt
        retailer (str): where receipt is from
        purchaseDate (date): date of purchase
        purchaseTime (time): time of purchase
        items (list[items]): items purchased
        total (float): total spent
    """
    id: UUID4 = Field(default_factory=uuid.uuid4)
    retailer: str = Field()
    purchaseDate: date = Field()
    purchaseTime: time = Field()
    items: List[Items] = Field()
    total: float = Field()


class CreateReceiptResponse(BaseModel):
    id: UUID4 = Field


class PointsResponse(BaseModel):
    points: int = Field()