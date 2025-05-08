from pydantic import BaseModel

class Keyword(BaseModel):
    id: int | None
    porcentage: float | None
    keyword: str | None
    max_page: int | None
    store_id: int | None
    active: bool | None
    alert_new: bool | None
    category: str | None
    blacklist: str | None
    sort: str | None
    landing_url: str | None
    
    '''

    La funcion set_data no hace falta, con el constructor ya puedo instanciar objetos a los que puedo modificar sus atributos cuando quiera

    keyw = Keyword(id=111,active=True,keyword="monitor")
    keyw.active = False


    '''
    def set_data (
        id,
        porcentage,
        keyword,
        max_page,
        store_id,
        active,
        alert_new,
        category,
        blacklist,
        sort,
        landing_url
    ):
        self.id = id
        self.porcentage = porcentage
        self.keyword = keyword
        self.max_page = max_page
        self.store_id = store_id
        self.active = active
        self.alert_new = alert_new
        self.category = category
        self.blacklist = blacklist
        self.sort = sort
        self.landing_url = landing_url

