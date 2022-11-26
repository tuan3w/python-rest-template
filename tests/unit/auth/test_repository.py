from app.container import AppContainer
from app.modules.auth.model import UserCreate


def test_repository(container: AppContainer):
    auth_repo = container.user_repo()

    user = auth_repo.get_by_id(1)
    assert user == None

    new_user = auth_repo.create(UserCreate(username="test", password="test"))
    user = auth_repo.get_by_id(new_user.id)
    assert user != None
