from app.container import AppContainer
from app.modules.auth.model import UserCreate


def test_create_thread(container: AppContainer):
    user1 = container.user_repo().create(UserCreate(username="test1", password="test"))

    create_thread_usc = container.thread.create_thread()
    thread1 = create_thread_usc.create_thread("test1", user1.id)

    member = container.thread_repo().get_thread_member(thread1.id, user1.id)
    assert member is not None
    assert member.role == "admin"

    members = container.thread_repo().get_thread_members(thread1.id)
    assert len(members) == 1
