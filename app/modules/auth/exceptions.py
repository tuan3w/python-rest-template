from app.core.exceptions import AppException
from app.core.i18n import _
class UserExistedError(AppException):
    http_code = 409
    error = "user_existed"
    i18n_message = _('User existed')

class UserNotFound(AppException):
    http_code = 404
    error = 'user_not_found'
    i18n_message = _('User not found')

class InvalidPassword(AppException):
    http_code = 401
    error = 'invalid_password'
    i18n_message = _('Invalid password')