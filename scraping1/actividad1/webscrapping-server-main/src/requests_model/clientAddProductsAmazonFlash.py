from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class AmazonFlashProduct(Product):
    promotion_codes: List[dict] | list = []

class clientAddProductsAmazonFlash(BaseModel):
    storeId: int
    products: List[AmazonFlashProduct]