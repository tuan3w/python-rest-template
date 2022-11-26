import pytest

from app.core.exceptions import PermissionDeniedError
from app.modules.auth.model import UserCreate
from app.modules.message.model import Message
from app.container import AppContainer


def test_create_message_valid(container: AppContainer):
    user1 = container.user_repo().create(UserCreate(username="test1", password="test"))
    user2 = container.user_repo().create(UserCreate(username="test2", password="test"))

    create_thread_usc = container.thread.create_thread()
    thread1 = create_thread_usc.create_thread("test1", user1.id)

    create_msg_usc = container.message.create_thread_message()
    create_msg_usc.create_message(
        Message(thread_id=thread1.id, message="test", user_id=user1.id)
    )

    with pytest.raises(PermissionDeniedError):
        create_msg_usc.create_message(
            Message(thread_id=thread1.id, message="test", user_id=user2.id)
        )
