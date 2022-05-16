import pytest

from app.modules.auth.usecases import RegisterUserUsecase
from app.modules.auth.exceptions import UserExistedError
from tests.utils import init_test_container


def test_register():
    container = init_test_container()
    usecase: RegisterUserUsecase = container.auth.register()
    u = usecase.register('test', 'test')
    assert u != None

    with pytest.raises(UserExistedError):
        usecase.register('test', 'test')
