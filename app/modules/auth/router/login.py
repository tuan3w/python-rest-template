
from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from pydantic import BaseModel

from app.container import AppContainer
from app.modules.auth.usecases.login import LoginUsecase
from app.core.jwt import sign_jwt

from .router import router

class LoginRequest(BaseModel):
    username: str
    password: str

@router.post("/login")
@inject
def login(
    req: LoginRequest,
    usecase: LoginUsecase = Depends(Provide[AppContainer.auth.login])
):
    login = usecase.login(req.username, req.password)
    return {"data": {"token": sign_jwt(login.id, usecase.app.conf.jwt_secret)}}
