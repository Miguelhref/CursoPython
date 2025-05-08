from pydantic import BaseModel

class ClientRequest(BaseModel):
    storeName: str | None
    products: list | None
    storeId: int | None
    keywordId: int | None
    sku: str | None