from pydantic import BaseModel
from typing import List
from src.requests_model.Product import Product

class clientChekProductAmazonReaco(BaseModel):
    keywordId: int
    sku: str

export = clientChekProductAmazonReaco