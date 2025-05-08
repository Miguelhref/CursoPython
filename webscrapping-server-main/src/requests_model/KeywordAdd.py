from pydantic import BaseModel

class KeywordAdd(BaseModel):
    porcentage: int
    keyword: str
    max_page: int
    store_id: int
    active: bool = True
    alert_new: bool = True
    category: str | None
    blacklist: str | None
    sort: str | None
    landing_url: str | None

export = KeywordAdd