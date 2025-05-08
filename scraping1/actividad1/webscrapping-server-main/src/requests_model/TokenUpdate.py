from pydantic import BaseModel

class TokenUpdate(BaseModel):
    name: str | None
    active: bool | None

export = TokenUpdate