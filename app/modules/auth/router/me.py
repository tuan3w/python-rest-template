
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from pydantic import BaseModel

from app.container import AppContainer
from app.core.jwt import get_current_user
from app.modules.auth.exceptions import UserNotFound
from app.modules.auth.usecases.me import MyInfoUsecase

from .router import router


class UserInfoResponse(BaseModel):
    id: str
    username: str

@router.get('/me')
@inject
def me(
    user_id: int = Depends(get_current_user),
    usecase: MyInfoUsecase = Depends(Provide[AppContainer.auth.me])
):

    user = usecase.get_user(user_id)
    # should not happen
    if not user:
        raise UserNotFound()

    return {"data": UserInfoResponse(**user.dict())}
