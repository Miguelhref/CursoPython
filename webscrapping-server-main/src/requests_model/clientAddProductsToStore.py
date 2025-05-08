from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class clientAddProductsToStore(BaseModel):
    storeId: int
    products: List[Product]