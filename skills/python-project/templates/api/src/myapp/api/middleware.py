"""API middleware and exception handlers."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from myapp.core.exceptions import AppError


def setup_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "message": exc.message,
                    "code": exc.code,
                    **exc.context,
                }
            },
        )
