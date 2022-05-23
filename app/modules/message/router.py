from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import AppContainer
from app.core.jwt import get_current_user
from app.modules.message.container import AppUsecase, MessageContainer

from .usecases import (CreateThreadMessageUsecase, DeleteThreadMessageUsecase,
                       GetThreadMessagesUsecase, Message)

Container : MessageContainer = AppContainer.message
router = APIRouter(prefix='/threads/{thread_id}/messages', tags=["messages"])

@router.get("")
@inject
def get_thread_messages(
    thread_id: int,
    user_id: int = Depends(get_current_user),
    usecase: GetThreadMessagesUsecase = Depends(
        Provide[Container.get_thread_messages])
):
    messages = usecase.get_thread_messages_for_user(thread_id, user_id)
    return {"data": messages}


class CreateThreadMessageRequest(BaseModel):
    message: str


@router.post("")
@inject
def create_thread_message(
    thread_id: int,
    req: CreateThreadMessageRequest,
    user_id: int=Depends(get_current_user),
    usecase: CreateThreadMessageUsecase = Depends(
        Provide[Container.create_thread_message])
):
    msg = usecase.create_message(
        Message(thread_id=thread_id, user_id=user_id, message=req.message))
    return {"data": msg}


@router.delete("/{message_id}")
@inject
def delete_thread_message(
    thread_id: int,
    message_id: int,
    user_id: int = Depends(get_current_user),
    usecase: DeleteThreadMessageUsecase = Depends(
        Provide[Container.delete_thread_message])
):
    usecase.delete_message_for_user(user_id, message_id)
    return {"data": {"success": True}}