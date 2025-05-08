from pydantic import BaseModel

class Store(BaseModel):
    id: int | None
    name: str | None
    active: bool | None
    tg_chatid: int | None
    tg_chatid_bigdrop: int | None
    percentage_bigdrop: float | None


    #Ocurre lo mismo que con keyword.py
    
    def set_data ( 
        id,
        name,
        active,
        tg_chatid,
        tg_chatid_bigdrop,
        percentage_bigdrop
     ):
        self.id = id
        self.name = name
        self.active = active
        self.tg_chatid = tg_chatid
        self.tg_chatid_bigdrop = tg_chatid_bigdrop
        self.percentage_bigdrop = percentage_bigdrop

export = Store