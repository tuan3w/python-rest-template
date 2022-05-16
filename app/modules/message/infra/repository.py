
from typing import Optional

from sqlalchemy import Column, String, Integer

from app.core.database import Base
from app.core.repository import SQLRepository
from app.modules.message.model import Message

from ..repository import MessageRepository


class MessageInDb(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    thread_id = Column(String)
    message = Column(String)
    user_id = Column(Integer)


class SQLMessageRepository(SQLRepository, MessageRepository):
    def get_thread_messages(self, thread_id: str):
        with self.session_factory() as session:
            messages = session.query(MessageInDb).filter(
                MessageInDb.thread_id == thread_id).all()
            mapped_messages = [Message.from_orm(msg) for msg in messages]
            return mapped_messages

    def create_message(self, msg: Message) -> Message:
        with self.session_factory() as session:
            db_item = MessageInDb(**msg.dict())
            session.add(db_item)
            session.commit()
            session.refresh(db_item)
            return Message.from_orm(db_item)

    def delete_message(self, msg_id: int):
        with self.session_factory() as session:
            session.query(MessageInDb).filter(
                MessageInDb.id == msg_id).delete()

    def get_by_id(self, msg_id: int) -> Optional[Message]:
        with self.session_factory() as session:
            msg = session.query(MessageInDb).filter(
                MessageInDb.id == msg_id
            ).first()
            if not msg:
                return None
            return Message.from_orm(msg)
