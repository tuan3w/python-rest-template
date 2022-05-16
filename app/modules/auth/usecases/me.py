from app.core.usecase import AppUsecase
class MyInfoUsecase(AppUsecase):
    def get_user(self, user_id: int):
        return self.repo.user.get_by_id(user_id)