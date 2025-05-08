from pydantic import BaseModel
from typing import List

class AmazonAsinProduct(BaseModel):
    sku: str | None
    name: str | None
    price_new: float | None
    price_reaco: float | None
    pvp: float | None
    url_item: str | None
    sku: str | None

class clientAddProductsToAmazonAsin(BaseModel):
    storeId: int
    tableName: str
    currency: str
    products: List[AmazonAsinProduct]