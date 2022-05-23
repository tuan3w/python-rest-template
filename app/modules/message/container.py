from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.app import MyApp

from .usecases import (
    CreateThreadMessageUsecase,
    DeleteThreadMessageUsecase,
    GetThreadMessagesUsecase,
)


class MessageContainer(DeclarativeContainer):
    app: MyApp = providers.Dependency()
    get_thread_messages = providers.Singleton(GetThreadMessagesUsecase, app)
    create_thread_message = providers.Singleton(CreateThreadMessageUsecase, app)
    delete_thread_message = providers.Singleton(DeleteThreadMessageUsecase, app)
