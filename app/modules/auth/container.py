from dependency_injector import providers
from dependency_injector.containers import DeclarativeContainer

from .usecases import *


class AuthContainer(DeclarativeContainer):
    app = providers.Dependency()

    register = providers.Singleton(RegisterUserUsecase, app=app)
    login = providers.Singleton(LoginUsecase, app=app)
    me = providers.Singleton(MyInfoUsecase, app=app)
