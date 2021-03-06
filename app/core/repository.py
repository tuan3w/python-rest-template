from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy.orm import Session

from app.modules.auth.repository import UserRepository
from app.modules.message.repository import MessageRepository
from app.modules.thread.repository import ThreadRepository


class AppRepository(object):
    def __init__(
        self,
        user_repo: UserRepository,
        msg_repo: MessageRepository,
        thread_repo: ThreadRepository,
    ):
        self.user = user_repo
        self.message = msg_repo
        self.thread = thread_repo


class SQLRepository(object):
    def __init__(self, db: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = db
