from fastapi import APIRouter, Body, Depends
from psycopg2.errors import UniqueViolation, UndefinedColumn, ForeignKeyViolation

from src.models.Keyword import Keyword
from src.middlewares.jwt import JWTBearer
from src.helpers.ApiError import ApiError
from src.repository.Keyword import KeywordRepo

from src.requests_model.KeywordAdd import KeywordAdd
from src.requests_model.KeywordUpdate import KeywordUpdate

router = APIRouter()

@router.post("/keyword/add", dependencies=[Depends(JWTBearer())])
def add_keyword(keywordBody: KeywordAdd = Body(...)):
    porcentage = keywordBody.porcentage
    keyword = keywordBody.keyword.strip()
    max_page = keywordBody.max_page
    store_id = keywordBody.store_id
    active = keywordBody.active
    alert_new = keywordBody.alert_new
    category = keywordBody.category.strip() if keywordBody.category else None
    blacklist = keywordBody.blacklist.strip() if keywordBody.blacklist else None
    sort = keywordBody.sort.strip() if keywordBody.sort else None
    landing_url = keywordBody.landing_url.strip() if keywordBody.landing_url else None

    if (keyword == ""):
        raise ApiError(status=400, ok=False, reason="KEYWORD_IS_REQUIRED")

    if (KeywordRepo.keyword_exists_for_store(keyword, store_id)):
        raise ApiError(status=400, ok=False, reason="KEYWORD_ALREADY_EXISTS")

    try:
        keyword_added = KeywordRepo.add({
            "porcentage": porcentage,
            "keyword": keyword,
            "max_page": max_page,
            "store_id": store_id,
            "active": active,
            "alert_new": alert_new,
            "category": category,
            "blacklist": blacklist,
            "sort": sort,
            "landing_url": landing_url
        })

        return { "ok": True, "keyword": keyword_added }
    except ForeignKeyViolation as e:
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

@router.put("/keyword/update/{id}", dependencies=[Depends(JWTBearer())])
def update_keyword(id: int, keywordBody: KeywordUpdate = Body(...)):
    porcentage = keywordBody.porcentage
    keyword = keywordBody.keyword.strip() if keywordBody.keyword else None
    max_page = keywordBody.max_page
    store_id = keywordBody.store_id
    active = keywordBody.active
    alert_new = keywordBody.alert_new
    category = keywordBody.category.strip() if keywordBody.category else None
    blacklist = keywordBody.blacklist.strip() if keywordBody.blacklist else None
    sort = keywordBody.sort.strip() if keywordBody.sort else None
    landing_url = keywordBody.landing_url.strip() if keywordBody.landing_url else None

    if (keyword != None):
        if (keyword == ""):
            raise ApiError(status=400, ok=False, reason="KEYWORD_VALUE_ERROR_MISSING")

        if (store_id == None):
            keyword_query = KeywordRepo.get_by_id(id, "store_id")

            if (keyword_query == None):
                raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

            store_id = keyword_query['store_id']

        if (KeywordRepo.keyword_exists_for_store(keyword, store_id, id)):
            raise ApiError(status=400, ok=False, reason="KEYWORD_ALREADY_EXISTS")

    try:
        keyword_updated = KeywordRepo.update(id, {
            "porcentage": porcentage,
            "keyword": keyword,
            "max_page": max_page,
            "store_id": store_id,
            "active": active,
            "alert_new": alert_new,
            "category": category,
            "blacklist": blacklist,
            "sort": sort,
            "landing_url": landing_url
        }, "id")

        if (keyword_updated == None):
            raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

        return { "ok": True, "keyword": keyword_updated }
    except ForeignKeyViolation as e:
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

@router.delete("/keyword/delete/{id}", dependencies=[Depends(JWTBearer())])
def delete_keyword(id: int):
    keyword_deleted = KeywordRepo.delete(id)

    if (keyword_deleted == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

    return { "ok": True, "keyword": keyword_deleted }

@router.get("/keyword/getAll", dependencies=[Depends(JWTBearer())])
def list_keyword():
    return { "ok": True, "keywords": KeywordRepo.list() }

@router.get("/keyword/{id}", dependencies=[Depends(JWTBearer())])
def get_keyword(id: int):
    if (id < 1):
        raise ApiError(status=400, ok=False, reason="ID_IS_INVALID")

    keyword = KeywordRepo.get_by_id(id)

    if (keyword == None):
        raise ApiError(status=400, ok=False, reason="KEYWORD_NOT_FOUND")

    return { "ok": True, "keyword": keyword }

# todas las keywords por id de tienda
@router.get("/keyword/store/{store_id}", dependencies=[Depends(JWTBearer())])
def get_keywords_by_store(store_id: int):
    if store_id < 1:
        raise ApiError(status=400, ok=False, reason="STORE_ID_IS_INVALID")

    keywords = KeywordRepo.get_by_store_id(store_id)

    if not keywords:
        raise ApiError(status=400, ok=False, reason="STORE_ID_NOT_FOUND")

    return {"ok": True, "keywords": keywords}

export = router