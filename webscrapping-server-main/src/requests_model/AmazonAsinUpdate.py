from pydantic import BaseModel

class AmazonAsinUpdate(BaseModel):
    country: str
    asin: str | None
    name: str | None
    price_new_alert: float | None
    price_reaco_alert: float | None
    active: bool | None

export = AmazonAsinUpdate