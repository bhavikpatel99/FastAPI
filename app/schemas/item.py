from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemSchema(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category: Optional[str] = None

class ItemResponse(ItemSchema):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
