from pydantic import BaseModel

class Token(BaseModel):
    id: int | None
    name: str | None
    active: bool | None
    token: str | None

#No hace falta la funcion set_data, ocurre lo mismo que con Keyword

    def set_data ( 
        id,
        name,
        active,
        token
     ):
        self.id = id
        self.name = name
        self.active = active
        self.token = token

export = Token