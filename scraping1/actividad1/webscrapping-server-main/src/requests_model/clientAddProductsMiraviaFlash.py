from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class miraviaFlashProduct(Product):
    itemDiscount: str
    itemCurrentStock: int
    base_price: float

class clientAddProductsMiraviaFlash(BaseModel):
    storeId: int
    products: List[miraviaFlashProduct]