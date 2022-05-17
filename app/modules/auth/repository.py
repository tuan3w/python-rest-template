
from abc import ABC, abstractmethod
from typing import Optional

from .model import User


class UserRepository(ABC):
    @abstractmethod
    def get_user_by_username(self, username: str, shared_session=None) -> Optional[User]:
        pass

    @abstractmethod
    def create(self, user: User, shared_session=None) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: int, shared_session=None) -> Optional[User]:
        pass
