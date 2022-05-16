
from abc import ABC, abstractmethod
from typing import Optional

from .model import Message


class MessageRepository(ABC):
    @abstractmethod
    def get_thread_messages(self, thread_id: str):
        pass

    @abstractmethod
    def create_message(self, msg: Message) -> Message:
        pass

    @abstractmethod
    def delete_message(self, msg_id: int):
        pass

    @abstractmethod
    def get_by_id(self, msg_id: int) -> Optional[Message]:
        pass