import sys

from app.container import AppContainer


def init_test_container():
    container = AppContainer()
    container.conf.from_value(
        {"db_url": "sqlite://", "jwt_secret": "RPtR2KyTCaUvjvyAyZDHytgjdi24uhYz"}
    )
    container.wire(packages=[sys.modules["app"]])

    # init database
    container.db().create_database()

    return container
