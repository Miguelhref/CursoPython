from pydantic import BaseModel

class TokenAdd(BaseModel):
    name: str
    active: bool = True

export = TokenAdd