from pydantic import BaseModel

class StoreAdd(BaseModel):
    name: str
    active: bool = True
    tg_chatid: int
    tg_chatid_bigdrop: int | None
    percentage_bigdrop: int | None

export = StoreAdd