from pydantic import BaseModel, Field, UUID4
from datetime import date, time
from typing import List
import uuid
class Items(BaseModel):
    shortDescription: str = Field()
    price: float = Field()


class Receipt(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    retailer: str = Field()
    purchaseDate: date = Field()
    purchaseTime: time = Field()
    items: List[Items] = Field()
    total: float = Field()


class CreateReceiptResponse(BaseModel):
    id: UUID4 = Field