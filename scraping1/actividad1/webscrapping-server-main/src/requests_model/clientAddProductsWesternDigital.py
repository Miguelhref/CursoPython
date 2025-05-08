from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class WesternDigital(BaseModel):
    name: str
    price: float | None
    stockLevel: int | None
    code: str | None

class clientAddProductsWesternDigital(BaseModel):
    storeId: int
    products: List[WesternDigital]