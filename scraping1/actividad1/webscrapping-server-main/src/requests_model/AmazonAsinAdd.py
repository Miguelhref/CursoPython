from pydantic import BaseModel

class AmazonAsinAdd(BaseModel):
    country: str
    asin: str
    name: str
    price_new_alert: float
    price_reaco_alert: float
    active: bool = True

export = AmazonAsinAdd