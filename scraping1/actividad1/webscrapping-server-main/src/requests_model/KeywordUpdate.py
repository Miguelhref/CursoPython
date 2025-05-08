from pydantic import BaseModel

class KeywordUpdate(BaseModel):
    porcentage: int | None
    keyword: str | None
    max_page: int | None
    store_id: int | None
    active: bool = True
    alert_new: bool = True
    category: str | None
    blacklist: str | None
    sort: str | None
    landing_url: str | None

export = KeywordUpdate