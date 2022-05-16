from typing import Optional

from sqlalchemy import Column, Integer, String

from app.core.repository import SQLRepository
from app.modules.auth.model import User
from app.modules.auth.repository import UserRepository
from app.modules.message.infra.repository import Base


class UserInDb(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)


class SQLUserRepository(SQLRepository, UserRepository):
    def get_user_by_username(self, username: str) -> Optional[User]:
        with self.session_factory() as session:
            user = session.query(UserInDb).filter(
                UserInDb.username == username).first()
            if not user:
                return None

            return User.from_orm(user)

    def create(self, user: User):
        with self.session_factory() as session:
            user = UserInDb(**user.dict())
            session.add(user)
            session.commit()
            session.refresh(user)

            return User.from_orm(user)

    def get_by_id(self, user_id: int) -> Optional[User]:
        with self.session_factory() as session:
            user = session.query(UserInDb).filter(
                UserInDb.id == user_id).first()
            if not user:
                return None
            return User.from_orm(user)
