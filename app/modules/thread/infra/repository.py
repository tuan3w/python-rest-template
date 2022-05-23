from typing import List, Optional

from sqlalchemy import Column, ForeignKey, Integer, String

from app.core.repository import SQLRepository
from app.modules.message.infra.repository import Base
from app.modules.thread.model import ChatThread, ChatThreadMember
from app.modules.thread.repository import ThreadRepository


class ChatThreadInDb(Base):
    __tablename__ = "threads"
    id = Column(Integer, primary_key=True)
    name = Column(String(256))
    owner_id = Column(Integer)


class ChatThreadMemberInDb(Base):
    __tablename__ = "thread_members"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    thread_id = Column(Integer, ForeignKey("threads.id"))
    role = Column(String)


class SQLThreadRepository(SQLRepository, ThreadRepository):
    def get_all_threads_for_user(self, user_id: str) -> List[ChatThread]:
        with self.session_factory() as session:
            threads = (
                session.query(ChatThreadInDb)
                .filter(ChatThreadInDb.owner_id == user_id)
                .all()
            )
            return [ChatThread.from_orm(thread) for thread in threads]

    def get_by_id(self, thread_id: str, shared_session=None) -> Optional[ChatThread]:
        with self.session_factory(shared_session) as session:
            thread = (
                session.query(ChatThreadInDb)
                .filter(ChatThreadInDb.id == thread_id)
                .one_or_none()
            )
            if not thread:
                return None
            return ChatThread.from_orm(thread)

    def create(self, thread: ChatThread, shared_session=None) -> ChatThread:
        with self.session_factory(shared_session) as session:
            item_db = ChatThreadInDb(**thread.dict())
            session.add(item_db)

            if not shared_session:
                session.commit()

            session.refresh(item_db)

            return ChatThread.from_orm(item_db)

    def delete(self, thread_id: int, shared_session=None):
        with self.session_factory(shared_session) as session:
            session.query(ChatThreadInDb).filter(
                ChatThreadInDb.id == thread_id
            ).delete()

            if not shared_session:
                session.commit()

    def get_thread_members(
        self, thread_id: int, shared_session=None
    ) -> List[ChatThreadMember]:
        with self.session_factory(shared_session) as session:
            thread_members = (
                session.query(ChatThreadMemberInDb)
                .filter(ChatThreadMemberInDb.thread_id == thread_id)
                .all()
            )

            return [ChatThreadMember.from_orm(member) for member in thread_members]

    def get_thread_member(
        self, thread_id: int, user_id: int, shared_session=None
    ) -> Optional[ChatThreadMember]:
        with self.session_factory(shared_session) as session:
            thread_member = (
                session.query(ChatThreadMemberInDb)
                .filter(ChatThreadMemberInDb.user_id == user_id)
                .filter(ChatThreadMemberInDb.thread_id == thread_id)
                .first()
            )
            if not thread_member:
                return None
            return ChatThreadMember.from_orm(thread_member)

    def remove_thread_member(self, thread_id: int, user_id: int, shared_session=None):
        with self.session_factory(shared_session) as session:
            session.query(ChatThreadMemberInDb).filter(
                ChatThreadMemberInDb.thread_id == thread_id
            ).filter(ChatThreadMemberInDb.user_id == user_id).delete()

            if not shared_session:
                session.commit()

    def add_thread_member(
        self, thread_id: int, user_id: int, role: str, shared_session=None
    ):
        with self.session_factory(shared_session) as session:
            member = ChatThreadMemberInDb(
                user_id=user_id, thread_id=thread_id, role=role
            )
            session.add(member)

            if not shared_session:
                session.commit()

            session.refresh(member)

            return ChatThreadMember.from_orm(member)
