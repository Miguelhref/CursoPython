from fastapi import APIRouter, Body, Depends
from psycopg2.errors import UniqueViolation, UndefinedColumn

from src.requests_model.StoreAdd import StoreAdd
from src.requests_model.StoreUpdate import StoreUpdate

from src.models.Store import Store
from src.middlewares.jwt import JWTBearer
from src.helpers.ApiError import ApiError
from src.repository.Store import StoreRepo

from message_scheduler import message_scheduler

router = APIRouter()

@router.post("/store/add", dependencies=[Depends(JWTBearer())])
def add_store(store: StoreAdd = Body(...)):
    name = store.name.strip() if store.name else ''
    active = store.active
    tg_chatid = store.tg_chatid
    tg_chatid_bigdrop = store.tg_chatid_bigdrop
    percentage_bigdrop = store.percentage_bigdrop

    if (name == ""):
        raise ApiError(status=400, ok=False, reason="NAME_VALUE_ERROR_MISSING")

    try:
        store_added = StoreRepo.add({
            "name": name,
            "active": active,
            "tg_chatid": tg_chatid,
            "tg_chatid_bigdrop": tg_chatid_bigdrop,
            "percentage_bigdrop": percentage_bigdrop
        })

        message_scheduler.initialize_scheduler()

        return { "ok": True, "store": store_added }
    except UniqueViolation as e:
        raise ApiError(status=400, ok=False, reason="STORE_ALREADY_EXISTS")

@router.put("/store/update/{id}", dependencies=[Depends(JWTBearer())])
def update_store(id: int, store: StoreUpdate = Body(...)):
    name = store.name.strip() if store.name else None
    active = store.active
    tg_chatid = store.tg_chatid
    tg_chatid_bigdrop = store.tg_chatid_bigdrop
    percentage_bigdrop = store.percentage_bigdrop

    try:
        store_updated = StoreRepo.update(id, {
            "name": name,
            "active": active,
            "tg_chatid": tg_chatid,
            "tg_chatid_bigdrop": tg_chatid_bigdrop,
            "percentage_bigdrop": percentage_bigdrop
        }, "id")

        if (store_updated == None):
            raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

        message_scheduler.initialize_scheduler()

        return { "ok": True, "store": store_updated }
    except UniqueViolation as e:
        raise ApiError(status=400, ok=False, reason="STORE_ALREADY_EXISTS")

@router.delete("/store/delete/{id}", dependencies=[Depends(JWTBearer())])
def delete_store(id: int):
    store_deleted = StoreRepo.delete(id, 'tg_chatid, tg_chatid_bigdrop')

    if (store_deleted == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    message_scheduler.initialize_scheduler()

    return { "ok": True, "store": store_deleted }

@router.get("/store/getAll", dependencies=[Depends(JWTBearer())])
def list_store():
    return { "ok": True, "stores": StoreRepo.list() }

@router.get("/store/{id}", dependencies=[Depends(JWTBearer())])
def get_store(id: int):
    store = StoreRepo.get_by_id(id)

    if (store == None):
        raise ApiError(status=400, ok=False, reason="STORE_NOT_FOUND")

    return { "ok": True, "store": store }

export = router