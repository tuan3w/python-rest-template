import sys

import pytest

from app.container import AppContainer


@pytest.fixture()
def container():
    container = AppContainer()
    container.conf.from_value(
        {"db_url": "sqlite://", "jwt_secret": "RPtR2KyTCaUvjvyAyZDHytgjdi24uhYz"}
    )
    container.wire(packages=[sys.modules["app"]])

    # init database
    container.db().create_database()

    return container
