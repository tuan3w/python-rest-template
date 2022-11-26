from asyncio.log import logger
from typing import Any, Optional

from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from .i18n import T, _


class AppException(Exception):
    i18n_message = _("Internal error")
    http_code = 400
    error = "internal_error"

    def __init__(
        self,
        code: Optional[int] = None,
        error_details: Any = None,
        **params,
    ):
        self.code = code
        self._params = params
        self.message = self.i18n_message
        self.error_details = error_details

    def translate(self, locale="en"):
        self.message = T(self.i18n_message, locale=locale, **self._params)

    def to_json(self):
        res = {
            "error": self.error,
            "message": self.message,
        }
        if self.error_details is not None:
            res["error_details"] = self.error_details

        if self.code is not None:
            res["code"] = self.code
        return res


class UserNotInThreadError(AppException):
    http_code = 403
    i18n_message = _("User isn't in this thread")
    error = "user_not_in_thread"


class UserNotFoundError(AppException):
    http_code = 404
    i18n_message = _("User not found")
    error = "user_not_found"


class PermissionDeniedError(AppException):
    http_code = 403
    i18n_message = _("You don't have permission to thread")
    error = "permission_denied"


class InternalServerError(AppException):
    http_code = 500
    i18n_message = _("Internal server error")
    error = "internal_error"


class UnAuthorizedError(AppException):
    http_code = 401
    i18n_message = _("Unauthorized")
    error = "unauthorized"


class ParamError(AppException):
    http_code = 400
    i18n_message = _("Invalid parameters")
    error = "invalid_parameters"


class DatabaseError(AppException):
    http_code = 500
    i18n_message = _("An database error has occured")
    error = "database_error"


def _translate_error_message(err: AppException, req: Request):
    # some http client will pass default header with default value
    #  'en-Us,en;q=0.9'
    locale = req.headers.get("accept-language", "vi")
    err.translate(locale)


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_error_handler(req: Request, err: AppException):
        if err.http_code >= 500:
            # masked error
            logger.error("Internal server error: {}".format(err.error_details))
            err = InternalServerError(error_details=[])

        _translate_error_message(err, req)

        return JSONResponse(
            status_code=err.http_code, content=jsonable_encoder(err.to_json())
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception_handler(
        req: Request, err: RequestValidationError
    ):
        new_err = ParamError(error_details=err.errors())
        _translate_error_message(new_err, req)

        return JSONResponse(
            status_code=new_err.http_code, content=jsonable_encoder(new_err.to_json())
        )
