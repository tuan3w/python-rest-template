from app.core.exceptions import PermissionDeniedError, UserNotFoundError
from app.core.usecase import AppUsecase
from app.modules.thread.model import ChatThread


class GetUserThreads(AppUsecase):
    def get_user_threads(self, user_id: int):
        threads = self.repo.thread.get_all_threads_for_user(user_id)
        return threads


class GetThreadUsecase(AppUsecase):
    def get_thread_for_user(self, thread_id: int, user_id: int):
        thread = self.repo.thread.get_by_id(thread_id)
        thread_member = self.repo.thread.get_thread_member(thread_id, user_id)
        if not thread_member:
            raise PermissionDeniedError()
        return thread


class CreateThreadUsecase(AppUsecase):
    def create_thread(self, name: str, owner_id: int):
        thread = self.repo.thread.create(ChatThread(owner_id=owner_id, name=name))
        self.repo.thread.add_thread_member(thread.id, owner_id, "admin")
        return thread


class GetThreadMembers(AppUsecase):
    def get_thread_members_for_user(self, thread_id: int, user_id: int):
        thread_member = self.repo.thread.get_thread_member(thread_id, user_id)
        if not thread_member:
            raise PermissionDeniedError()
        return self.repo.thread.get_thread_members(thread_id)


class AddMemberToThread(AppUsecase):
    def add_member_to_thread(
        self, thread_id: int, user_id: int, target_user_id: int, role: str
    ):
        thread_member = self.repo.thread.get_thread_member(self, thread_id, user_id)
        if not thread_member:
            raise PermissionDeniedError()
        if thread_member.role != "admin":
            raise PermissionDeniedError()

        target_user = self.repo.user.get_by_id(target_user_id)
        if not target_user:
            raise UserNotFoundError()

        thread_member = self.repo.thread.get_thread_member(
            self, thread_id, target_user_id
        )
        if thread_member:
            # already in the target thread, ignore
            return
        self.repo.thread.add_thread_member(thread_id, target_user_id, role)


class RemoveMemberFromThreadUsecase(AppUsecase):
    def remove_member(self, thread_id: int, user_id: int, target_user_id: int):
        thread_member = self.repo.thread.get_thread_member(self, thread_id, user_id)
        if not thread_member:
            raise PermissionDeniedError()
        if thread_member.role != "admin":
            raise PermissionDeniedError()

        target_user = self.repo.user.get_by_id(target_user_id)
        if not target_user:
            raise UserNotFoundError()

        self.repo.thread.remove_thread_member(thread_id, target_user_id)
