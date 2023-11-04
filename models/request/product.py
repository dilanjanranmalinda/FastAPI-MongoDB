from pydantic import BaseModel
from typing import Optional


class ProductCreation(BaseModel):
    product_name: str
    price: float
    description: Optional[str]


