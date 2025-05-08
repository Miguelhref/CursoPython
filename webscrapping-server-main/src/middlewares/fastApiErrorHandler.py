from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from starlette.exceptions import HTTPException as StarletteHTTPException

from src.helpers.ApiError import ApiError

def fastApiErrorHandler(app):

    @app.exception_handler(ApiError)
    def fastApiErrorHandler(request, exc):
        return JSONResponse(
            status_code=exc.status,
            content={
                "ok": False,
                "reason": exc.reason,
                "message": exc.message
            }
        )

    @app.exception_handler(Exception)
    def http_exception_handler(request, exc):
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "reason": "SERVER_ERROR"
            }
        )

    @app.exception_handler(RequestValidationError)
    def http_exception_handler(request, exc):
        errors = exc.errors()

        first_error = errors[0]

        if (first_error['type'] == 'value_error.jsondecode'):
            return JSONResponse(
                status_code=400,
                content={
                    "ok": False,
                    "reason": "INVALID_JSON"
                }
            )

        last_loc = first_error['loc'][-1]
        parse_to_reason = (last_loc + '_' + first_error['type'].replace('.', '_')).upper()

        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "reason": parse_to_reason,
            }
        )