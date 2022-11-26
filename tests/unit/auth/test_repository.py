from app.modules.auth.model import UserCreate
from tests.utils import init_test_container


def test_repository():
    container = init_test_container()
    auth_repo = container.user_repo()

    user = auth_repo.get_by_id(1)
    assert user == None

    new_user = auth_repo.create(UserCreate(username="test", password="test"))
    user = auth_repo.get_by_id(new_user.id)
    assert user != None
