
from app.core.exceptions import AppException
from app.core.i18n import _


class ThreadNotFound(AppException):
    http_code = 404
    error = 'thread_not_found'
    i18n_message = _('Thread not found')

class MessageNotFound(AppException):
    i18n_message = _('Message not found')
    http_code = 404
    error = 'message_not_found'