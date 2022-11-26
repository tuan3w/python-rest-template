from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from app.core.app import MyApp

from .usecases import (
    AddMemberToThread,
    CreateThreadUsecase,
    GetThreadMembers,
    GetThreadUsecase,
    GetUserThreads,
    RemoveMemberFromThreadUsecase,
)


class ThreadContainer(DeclarativeContainer):
    app = providers.Dependency(MyApp)
    get_user_threads = providers.Singleton(GetUserThreads, app)
    get_thread = providers.Singleton(GetThreadUsecase, app)
    create_thread = providers.Singleton(CreateThreadUsecase, app)
    get_thread_members = providers.Singleton(GetThreadMembers, app)
    add_member_to_thread = providers.Singleton(AddMemberToThread, app)
    remove_member_from_thread = providers.Singleton(RemoveMemberFromThreadUsecase, app)
