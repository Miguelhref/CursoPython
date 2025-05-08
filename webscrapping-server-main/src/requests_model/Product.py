from pydantic import BaseModel

class Product(BaseModel):
    sku: str | None
    url_item: str | None
    url_img: str | None
    name: str | None
    price: float | None
    pvp: float | None
    """ coupon: dict | None """

export = Product