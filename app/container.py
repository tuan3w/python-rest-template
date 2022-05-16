from app.core.app import MyApp
from app.core.conf import AppConf
from app.core.database import Database
from app.core.repository import AppRepository
from app.modules.auth.container import AuthContainer
from app.modules.auth.infra.repository import SQLUserRepository
from app.modules.message.container import MessageContainer
from app.modules.message.infra.repository import SQLMessageRepository
from app.modules.thread.container import ThreadContainer
from app.modules.thread.infra.repository import SQLThreadRepository


from dependency_injector import providers, containers
from dependency_injector.containers import DeclarativeContainer


class AppContainer(DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["app"])

    conf = providers.Configuration(yaml_files=["config.yaml"])
    app_conf = providers.Singleton(AppConf, conf)

    db = providers.Singleton(Database, conf=app_conf)
    msg_repo = providers.Singleton(
        SQLMessageRepository,
        db=db.provided.session)
    thread_repo = providers.Singleton(
        SQLThreadRepository,
        db=db.provided.session
    )
    user_repo = providers.Singleton(
        SQLUserRepository,
        db=db.provided.session
    )
    app_repo = providers.Singleton(
        AppRepository, user_repo=user_repo, thread_repo=thread_repo, msg_repo=msg_repo)
    app = providers.Singleton(
        MyApp,
        conf=app_conf,
        repo=app_repo,
    )

    # services
    auth = providers.Container(
        AuthContainer,
        app=app
    )
    thread = providers.Container(
        ThreadContainer,
        app=app
    )
    message = providers.Container(
        MessageContainer,
        app=app
    )
