import pytest

from app.container import AppContainer
from app.modules.auth.exceptions import UserExistedError
from app.modules.auth.usecases import RegisterUserUsecase


def test_register(container: AppContainer):
    usecase: RegisterUserUsecase = container.auth.register()
    u = usecase.register("test", "test")
    assert u != None

    with pytest.raises(UserExistedError):
        usecase.register("test", "test")
