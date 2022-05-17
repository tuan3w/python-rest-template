
from abc import ABC, abstractmethod
from typing import Optional

from .model import Message


class MessageRepository(ABC):
    @abstractmethod
    def get_thread_messages(self, thread_id: str, shared_session=None):
        pass

    @abstractmethod
    def create_message(self, msg: Message, shared_session=None) -> Message:
        pass

    @abstractmethod
    def delete_message(self, msg_id: int, shared_session=None):
        pass

    @abstractmethod
    def get_by_id(self, msg_id: int, shared_session=None) -> Optional[Message]:
        pass