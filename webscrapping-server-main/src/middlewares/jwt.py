
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.helpers.ApiError import ApiError

from src.helpers.jwt import decodeJWT


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = False):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # compatibility with old scrapers
        authorization = request.headers.get("Authorization")
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise ApiError(status=403, reason="NOT_ALLOWED")
            if not self.verify_jwt(credentials.credentials):
                raise ApiError(status=403, reason="NOT_ALLOWED", message="Invalid token or expired token.")
            return credentials.credentials
        else:
            if (authorization):
                if not self.verify_jwt(authorization):
                    raise ApiError(status=403, reason="NOT_ALLOWED", message="Invalid token or expired token.")
                return authorization
            else:
                raise ApiError(status=403, reason="NOT_ALLOWED", message="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            payload = decodeJWT(jwtoken)
        except:
            payload = None

        if payload:
            isTokenValid = True

        return isTokenValid



