from abc import ABC, abstractmethod
from typing import Any, List, Optional

from .model import ChatThread, ChatThreadCreate, ChatThreadMember


class ThreadRepository(ABC):
    @abstractmethod
    def get_by_id(
        self, thread_id: int, shared_session: Any = None
    ) -> Optional[ChatThread]:
        pass

    @abstractmethod
    def create(self, thread: ChatThreadCreate, shared_session=None) -> ChatThread:
        pass

    @abstractmethod
    def get_all_threads_for_user(
        self, user_id: int, shared_session=None
    ) -> List[ChatThread]:
        pass

    @abstractmethod
    def delete(self, thread_id: int, shared_session=None):
        pass

    @abstractmethod
    def get_thread_members(
        self, thread_id: int, shared_session=None
    ) -> List[ChatThreadMember]:
        pass

    @abstractmethod
    def get_thread_member(
        self, thread_id: int, user_id: int, shared_session=None
    ) -> Optional[ChatThreadMember]:
        pass

    @abstractmethod
    def add_thread_member(
        self, thread_id: int, user_id: int, role: str, shared_session=None
    ) -> ChatThreadMember:
        pass

    @abstractmethod
    def remove_thread_member(self, thread_it: int, user_id: int, shared_session=None):
        pass
