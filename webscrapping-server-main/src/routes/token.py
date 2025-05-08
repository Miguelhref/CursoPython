from fastapi import APIRouter, Body, Depends, HTTPException

from src.models.Token import Token

from src.requests_model.TokenAdd import TokenAdd
from src.requests_model.TokenUpdate import TokenUpdate

from src.middlewares.jwt import JWTBearer
from src.helpers.jwt import create_access_token
from src.helpers.ApiError import ApiError
from src.repository.Token import TokenRepo

router = APIRouter()

@router.post("/token/add")
def add_token(token: TokenAdd = Body(...)):
    token.name = token.name.strip()

    if (token.name == ""):
        raise ApiError(status=400, ok=False, reason="NAME_VALUE_ERROR_MISSING")

    query_token = TokenRepo.get_by_name(token.name)

    if (query_token):
        raise ApiError(status=400, ok=False, reason="NAME_ALREADY_EXISTS")

    access_token = create_access_token()

    token_added = TokenRepo.add({ "name": token.name, "active": token.active, "token": access_token }, "id, token")

    return {
        "ok": True,
        "token": token_added
    }

@router.put("/token/update/{id}", dependencies=[Depends(JWTBearer())])
def update_token(id: int, token: TokenUpdate = Body(...)):
    if (token.name != None):
        token.name = token.name.strip()

        if (token.name == ""):
            raise ApiError(status=400, ok=False, reason="NAME_VALUE_ERROR_MISSING")

        query_token_name = TokenRepo.get_by_name(token.name)

        if (query_token_name and query_token_name['id'] != id):
            raise ApiError(status=400, ok=False, reason="NAME_ALREADY_EXISTS")

    token_updated = TokenRepo.update(id, {
        "name": token.name,
        "active": token.active
    }, "id")

    if (token_updated == None):
        raise ApiError(status=400, ok=False, reason="TOKEN_NOT_FOUND")

    return {
        "ok": True,
        "token": token_updated
    }

@router.delete("/token/delete/{id}", dependencies=[Depends(JWTBearer())])
def delete_token(id: int):
    token_removed = TokenRepo.delete(id)

    if (token_removed == None):
        raise ApiError(status=400, ok=False, reason="TOKEN_NOT_FOUND")

    return { "ok": True, "token": token_removed }

@router.get("/token/getAll", dependencies=[Depends(JWTBearer())])
def list_token():
    return {"ok": True, "tokens": TokenRepo.list()}

@router.get("/token/{id}", dependencies=[Depends(JWTBearer())])
def get_token(id: int):
    token = TokenRepo.get_by_id(id)

    if (token == None):
        raise ApiError(status=400, ok=False, reason="TOKEN_NOT_FOUND")

    return { "ok": True, "token": token }

export = router