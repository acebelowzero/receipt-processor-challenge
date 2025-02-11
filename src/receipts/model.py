from pydantic import BaseModel, UUID4
from sqlmodel import SQLModel, Field, Relationship
from datetime import date, time
from typing import List
import uuid

from sqlalchemy import ForeignKey


class Receipt(SQLModel, table=True):
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

    idx: int = Field(primary_key=True, index=True)
    id: UUID4 = Field(default_factory=uuid.uuid4, sa_column_kwargs={"unique": True})
    retailer: str = Field()
    purchaseDate: date = Field()
    purchaseTime: time = Field()
    items: List["Item"] = Relationship(back_populates="receipt", cascade_delete=True)
    total: float = Field()


class Item(SQLModel, table=True):
    """Item schema

    Attributes:
        shortDescription (str): description of
            the item

        price (float): price of the item

    """

    idx: int = Field(primary_key=True, index=True)
    receipt_id: UUID4 = Field(foreign_key="receipt.id")
    shortDescription: str = Field()
    price: float = Field()
    receipt: Receipt | None = Relationship(back_populates="items")


class Point(SQLModel, table=True):
    idx: int = Field(primary_key=True, index=True)
    id: UUID4 = Field(foreign_key="receipt.id")
    points: int = Field()
