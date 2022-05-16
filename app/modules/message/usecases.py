from app.core.exceptions import PermissionDenied
from app.core.usecase import AppUsecase
from app.modules.message.exceptions import MessageNotFound, ThreadNotFound
from app.modules.message.model import Message

class GetThreadMessagesUsecase(AppUsecase):
    def get_thread_messages_for_user(self, thread_id: int, user_id: int):
        thread = self.repo.thread.get_by_id(thread_id)
        if not thread:
            raise ThreadNotFound()

        thread_member = self.repo.thread.get_thread_member(thread_id, user_id)
        if not thread_member:
            raise PermissionDenied()

        return self.repo.message.get_thread_messages(thread_id)

class CreateThreadMessageUsecase(AppUsecase):
    def create_message(self, msg: Message) -> Message:
        thread = self.repo.thread.get_by_id(msg.thread_id)
        if not thread:
            raise ThreadNotFound()

        thread_member = self.repo.thread.get_thread_member(msg.thread_id, msg.user_id)
        if not thread_member:
            raise PermissionDenied()

        return self.repo.message.create_message(msg)

class DeleteThreadMessageUsecase(AppUsecase):
    def delete_message_for_user(self, user_id: int, msg_id: int):
        msg = self.repo.message.get_by_id(msg_id)
        if not msg:
            raise MessageNotFound()
        if msg.owner_id != user_id:
            raise PermissionDenied()

        msg = self.repo.message.get_by_id(msg_id)
        if not msg:
            raise MessageNotFound()
