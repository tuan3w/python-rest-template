from app.core.usecase import AppUsecase
from app.modules.auth.exceptions import UserExistedError
from app.modules.auth.model import User
from app.modules.auth.utils import hash_password
class RegisterUserUsecase(AppUsecase):
    def register(self, username: str, passwd: str) -> User:
        user = self.repo.user.get_user_by_username(username)
        if user:
            raise UserExistedError()

        hashed_passwd = hash_password(passwd)
        user = self.repo.user.create(User(username=username, password=hashed_passwd))
        return user