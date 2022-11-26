import logging
import sys

from dependency_injector.wiring import inject
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.container import AppContainer
from app.core.exceptions import add_error_handlers
from app.modules.auth.router import router as auth_router
from app.modules.messages.router import router as msg_router
from app.modules.threads.router import router as thread_router


@inject
def create_app() -> FastAPI:
    # disable sqlalchemy logging
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.getLogger("sqlalchemy").disabled = True

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    add_error_handlers(app)

    app_container = AppContainer()
    app_container.conf.from_yaml("./config.yaml")
    app_container.init_resources()

    # NOTE: dependency_injector try to scan all directory in `app`
    # package, so be sure to add __init__.py to any subfolders
    # TODO: better solution to inject variables automatically
    app_container.wire(packages=[sys.modules["app"]])
    app_container.check_dependencies()

    # init routers
    app.include_router(auth_router)
    app.include_router(msg_router)
    app.include_router(thread_router)
    return app


app = create_app()
# uvicorn.run(app)
