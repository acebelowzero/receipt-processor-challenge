import logging
from src.utils.config import settings
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from http import HTTPStatus
from src.exceptions import exceptions as HTTPExceptions
from src.repo import exceptions as RepoExceptions
from pydantic import ValidationError
from fastapi.exceptions import RequestValidationError


logger = logging.getLogger(settings.ENVIRONMENT)


def setup_api_exceptions(app: FastAPI):
    @app.exception_handler(HTTPExceptions.BaseException)
    @app.exception_handler(HTTPExceptions.HTTP400BadRequestError)
    @app.exception_handler(HTTPExceptions.HTTP404NotFoundError)
    @app.exception_handler(HTTPExceptions.HTTP404NotFoundError)
    @app.exception_handler(RepoExceptions.ElementNotFoundError)
    async def custom_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        print(exc)
        return JSONResponse(
            status_code=exc.status_code, content={"message": exc.message}
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_error(request: Request, exc: Exception) -> JSONResponse:
        logger.error("request could not be processed: %s", exc)
        error_message = ""
        if exc.errors():
            error_message = (
                f"{exc.errors()[0].get('msg')}, {exc.errors()[0].get('loc')}"
            )

        code = HTTPStatus.UNPROCESSABLE_ENTITY
        return JSONResponse(status_code=code, content={"message": error_message})
