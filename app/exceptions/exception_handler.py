from fastapi import Request
from fastapi.responses import JSONResponse

from app.exceptions.custom_exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: Exception,
):

    if isinstance(exc, AppException):

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "message": exc.message,
            },
        )

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
        },
    )