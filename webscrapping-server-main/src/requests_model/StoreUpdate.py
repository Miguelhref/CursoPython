from pydantic import BaseModel

class StoreUpdate(BaseModel):
    name: str | None
    active: bool = True
    tg_chatid: int | None
    tg_chatid_bigdrop: int | None
    percentage_bigdrop: int | None

export = StoreUpdate