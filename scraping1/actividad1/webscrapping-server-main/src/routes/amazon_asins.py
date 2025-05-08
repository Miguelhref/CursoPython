from fastapi import APIRouter, Body, Depends
from psycopg2.errors import UniqueViolation, UndefinedColumn, UndefinedTable

from src.requests_model.AmazonAsinAdd import AmazonAsinAdd
from src.requests_model.AmazonAsinUpdate import AmazonAsinUpdate

from src.models.Store import Store
from src.middlewares.jwt import JWTBearer
from src.helpers.ApiError import ApiError

from src.repository.AmazonAsins import AmazonAsinsRepo

from message_scheduler import message_scheduler

router = APIRouter()

@router.post("/amazon_asins/add", dependencies=[Depends(JWTBearer())])
def add_store(amazonAsin: AmazonAsinAdd = Body(...)):
    country = amazonAsin.country.strip() if amazonAsin.country else ''
    asin = amazonAsin.asin.strip() if amazonAsin.asin else ''
    name = amazonAsin.name.strip() if amazonAsin.name else ''
    price_new_alert = amazonAsin.price_new_alert
    price_reaco_alert = amazonAsin.price_reaco_alert
    active = amazonAsin.active

    if (country == ""):
        raise ApiError(status=400, ok=False, reason="COUNTRY_VALUE_ERROR_MISSING")

    if (asin == ""):
        raise ApiError(status=400, ok=False, reason="ASIN_VALUE_ERROR_MISSING")

    if (name == ""):
        raise ApiError(status=400, ok=False, reason="NAME_VALUE_ERROR_MISSING")

    if (price_new_alert == 0):
        raise ApiError(status=400, ok=False, reason="PRICE_NEW_ALERT_VALUE_ERROR_MISSING")

    if (price_reaco_alert == 0):
        raise ApiError(status=400, ok=False, reason="PRICE_REACO_ALERT_VALUE_ERROR_MISSING")

    table_name = 'amazon_asins_' + country

    try:
        asin_added = AmazonAsinsRepo.add({
            "asin": asin,
            "name": name,
            "price_new_alert": price_new_alert,
            "price_reaco_alert": price_reaco_alert,
            "active": active
        }, table_name)

        return { "ok": True, "asin": asin_added }
    except UniqueViolation as e:
        raise ApiError(status=400, ok=False, reason="ASIN_ALREADY_EXISTS")
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="COUNTRY_NOT_FOUND")

@router.put("/amazon_asins/update/{id}", dependencies=[Depends(JWTBearer())])
def update_store(id: int, amazonAsin: AmazonAsinUpdate = Body(...)):
    country = amazonAsin.country.strip() if amazonAsin.country else ''
    asin = amazonAsin.asin.strip() if amazonAsin.asin else ''
    name = amazonAsin.name.strip() if amazonAsin.name else ''
    price_new_alert = amazonAsin.price_new_alert
    price_reaco_alert = amazonAsin.price_reaco_alert
    active = amazonAsin.active

    table_name = 'amazon_asins_' + country

    try:
        asin_updated = AmazonAsinsRepo.update(id, {
            "country": country,
            "asin": asin,
            "name": name,
            "price_new_alert": price_new_alert,
            "price_reaco_alert": price_reaco_alert,
            "active": active
        }, table_name, "id")

        if (asin_updated == None):
            raise ApiError(status=400, ok=False, reason="ASIN_NOT_FOUND")

        return { "ok": True, "asin": asin_updated }
    except UniqueViolation as e:
        raise ApiError(status=400, ok=False, reason="ASIN_ALREADY_EXISTS")
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="COUNTRY_NOT_FOUND")

@router.delete("/amazon_asins/delete/{country}/{asin}", dependencies=[Depends(JWTBearer())])
def delete_store(country: str, asin: str):
    table_name = 'amazon_asins_' + country

    try:
        asin_deleted = AmazonAsinsRepo.delete_by_asin(asin, table_name)

        if (asin_deleted == None):
            raise ApiError(status=400, ok=False, reason="ASIN_NOT_FOUND")

        return { "ok": True, "asin": asin_deleted }
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="COUNTRY_NOT_FOUND")

    return { "ok": False }

@router.get("/amazon_asins/{country}/getAll", dependencies=[Depends(JWTBearer())])
def list_store(country: str):
    table_name = 'amazon_asins_' + country

    try:
        return { "ok": True, "asins": AmazonAsinsRepo.list(table_name) }
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="COUNTRY_NOT_FOUND")

    return { "ok": False }

@router.get("/amazon_asins/{country}/{asin}", dependencies=[Depends(JWTBearer())])
def get_store(country: str, asin: str):
    table_name = 'amazon_asins_' + country

    try:
        query_asin = AmazonAsinsRepo.get_by_asin(asin, table_name)

        if (query_asin == None):
            raise ApiError(status=400, ok=False, reason="ASIN_NOT_FOUND")

        return { "ok": True, "asin": query_asin }
    except UndefinedTable as e:
        raise ApiError(status=400, ok=False, reason="COUNTRY_NOT_FOUND")

    return { "ok": False }

export = router