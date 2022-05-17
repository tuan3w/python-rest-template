from sqlite3 import InternalError
from xml.dom import ValidationErr
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError

from .i18n import _, T


class AppException(Exception):
    i18n_message = _('Internal error')
    http_code = 400
    error = "internal_error"

    def __init__(self,
                 code: int = None,
                 error_details: any = None,
                 **params,
                 ):
        self.code = code
        self._params = params
        self.message = self.i18n_message
        self.error_details = error_details

    def translate(self, locale='en'):
        self.message = T(self.i18n_message, locale=locale, **self._params)

    def to_json(self):
        res = {
            "error": self.error,
            "message": self.message,
        }
        if self.error_details is not None:
            res['error_details'] = self.error_details

        if self.code is not None:
            res["code"] = self.code
        return res


class UserNotInThread(AppException):
    http_code = 403
    i18n_message = _('User isn\'t in this thread')


class UserNotFound(AppException):
    http_code = 404
    i18n_message = _('User not found')
    error = 'user_not_found'


class PermissionDenied(AppException):
    http_code = 403
    i18n_message = _('You don\'t have permission to thread')
    error = 'permission_denied'


class InternalServerError(AppException):
    http_code = 500
    i18n_message = _('Internal server error')
    error = 'internal_error'

class UnAuthorized(AppException):
    http_code = 401
    i18n_message = _('Unauthorized')
    error = 'unauthorized'


class ParamError(AppException):
    http_code = 400
    i18n_message = _('Invalid parameters')
    error = 'invalid_parameters'

class DatabaseError(AppException):
    http_code = 500
    i18n_message = _('Internal server error')
    error = 'internal_error'


def add_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_error_handler(req: Request, err: AppException):
        # translate error
        # TODO: fixme
        # some http client will pass default header with default value
        #  'en-Us,en;q=0.9'
        # we need a way to find closest language
        user_locale = req.headers.get('accept-language', 'vi')
        err.translate(user_locale)

        return JSONResponse(
            status_code=err.http_code,
            content=jsonable_encoder(err.to_json())
        )

    @app.exception_handler(RequestValidationError)
    async def handle_validation_exception_handler(req: Request, err: RequestValidationError):
        new_err = ParamError(error_details=err.errors())
        user_locale = req.headers.get('accept-language', 'vi')
        new_err.translate(user_locale)

        return JSONResponse(
            status_code=new_err.http_code,
            content=jsonable_encoder(new_err.to_json())
        )

    @app.exception_handler(Exception)
    async def handle_internal_exception_handler(req: Request, err: Exception):
        #FIXME: mask sql errors here
        masked_err = InternalServerError(error_details=err)
        user_locale = req.headers.get('accept-language', 'vi')
        masked_err.translate(user_locale)

        return JSONResponse(
            status_code=masked_err.http_code,
            content=jsonable_encoder(masked_err.to_json())
        )
