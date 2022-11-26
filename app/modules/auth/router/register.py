from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from pydantic import BaseModel

from app.container import AppContainer
from app.core.jwt import sign_jwt
from app.modules.auth.usecases.register import RegisterUserUsecase

from .router import router

Container = AppContainer.auth


class RegisterUserRequest(BaseModel):
    username: str
    password: str


class RegisterUserResponse(BaseModel):
    token: str


@router.post("/register")
@inject
async def register(
    req: RegisterUserRequest,
    usecase: RegisterUserUsecase = Depends(Provide[AppContainer.auth.register]),
):
    user = usecase.register(req.username, req.password)
    return {"data": sign_jwt(user.id, usecase.app.conf.jwt_secret)}
