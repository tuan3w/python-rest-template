

from abc import ABC, abstractmethod
from typing import List, Optional

from .model import ChatThread, ChatThreadMember


class ThreadRepository(ABC):
    @abstractmethod
    def get_by_id(self, thread_id: int) -> Optional[ChatThread]:
        pass

    @abstractmethod
    def create(self, thread: ChatThread) -> ChatThread:
        pass

    @abstractmethod
    def get_all_threads_for_user(self, user_id: int) -> List[ChatThread]:
        pass

    @abstractmethod
    def delete(self, thread_id: int):
        pass

    @abstractmethod
    def get_thread_members(self, thread_id: int) -> List[ChatThreadMember]:
        pass

    @abstractmethod
    def get_thread_member(self, thread_id: int,
                          user_id: int) -> Optional[ChatThreadMember]:
        pass

    @abstractmethod
    def add_thread_member(self, thread_id: int, user_id: int, role: str) -> ChatThreadMember:
        pass

    @abstractmethod
    def remove_thread_member(self, thread_it: int, user_id: int):
        pass
