import pytest

from app.modules.auth.exceptions import UserExistedError
from app.modules.auth.usecases import RegisterUserUsecase
from app.container import AppContainer

def test_register(container: AppContainer):
    usecase: RegisterUserUsecase = container.auth.register()
    u = usecase.register("test", "test")
    assert u != None

    with pytest.raises(UserExistedError):
        usecase.register("test", "test")
