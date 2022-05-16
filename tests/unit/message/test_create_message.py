from app.modules.auth.model import User
import pytest
from app.modules.message.model import Message
from app.modules.thread.model import ChatThread
from tests.utils import init_test_container
from app.core.exceptions import PermissionDenied


def test_create_message_valid():
    container = init_test_container()
    user1 = container.user_repo().create(User(username='test1', password='test'))
    user2 = container.user_repo().create(User(username='test2', password='test'))

    create_thread_usc = container.thread.create_thread()
    thread1 = create_thread_usc.create_thread(
        "test1", user1.id)

    create_msg_usc = container.message.create_thread_message()
    create_msg_usc.create_message(
        Message(thread_id=thread1.id, message='test', user_id=user1.id))

    with pytest.raises(PermissionDenied):
        create_msg_usc.create_message(
            Message(thread_id=thread1.id, message='test', user_id=user2.id))
