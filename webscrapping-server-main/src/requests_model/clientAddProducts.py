from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class clientAddProducts(BaseModel):
    keywordId: int
    products: List[Product]