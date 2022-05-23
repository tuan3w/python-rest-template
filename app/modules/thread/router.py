from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.container import AppContainer
from app.core.jwt import get_current_user
from app.modules.thread.container import ThreadContainer

from .usecases import (
    AddMemberToThread,
    CreateThreadUsecase,
    GetThreadMembers,
    GetThreadUsecase,
    GetUserThreads,
    RemoveMemberFromThreadUsecase,
)

Container: ThreadContainer = AppContainer.thread
router = APIRouter(prefix="/threads", tags=["threads"])


@router.get("")
@inject
def get_all_threads(
    user_id: int = Depends(get_current_user),
    usecase: GetUserThreads = Depends(Provide[Container.get_user_threads]),
):
    threads = usecase.get_user_threads(user_id)
    return {"data": threads}


class CreateThreadRequest(BaseModel):
    name: str


@router.post("")
@inject
def create_thread(
    req: CreateThreadRequest,
    user_id: int = Depends(get_current_user),
    usecase: CreateThreadUsecase = Depends(Provide[Container.create_thread]),
):
    thread = usecase.create_thread(req.name, user_id)
    return {"data": thread}


@router.get("/{thread_id}")
@inject
def get_thread(
    thread_id: int,
    user_id: int = Depends(get_current_user),
    usecase: GetThreadUsecase = Depends(Provide[Container.get_thread]),
):
    thread = usecase.get_thread_for_user(thread_id, user_id)
    return {"data": thread}


@router.get("/{thread_id}/members")
@inject
def get_thread_members(
    thread_id: int,
    user_id: int = Depends(get_current_user),
    usecase: GetThreadMembers = Depends(Provide[Container.get_thread_members]),
):
    thread_members = usecase.get_thread_members_for_user(thread_id, user_id)
    return {"data": thread_members}


@router.delete("/{thread_id}/members")
@inject
def remove_member_from_thread(
    thread_id: int,
    user_id: int = Depends(get_current_user),
    usecase: AddMemberToThread = Depends(Provide[Container.add_member_to_thread]),
):
    usecase.add_member_to_thread(thread_id, user_id)
    return {"data": {"success": True}}


class RemoveMemberRequest(BaseModel):
    user_id: int


@router.delete("/{thread_id}/members")
@inject
def remove_member_from_thread(
    thread_id: int,
    req: RemoveMemberRequest,
    user_id: int = Depends(get_current_user),
    usecase: RemoveMemberFromThreadUsecase = Depends(
        Provide[Container.remove_member_from_thread]
    ),
):
    usecase.remove_member(thread_id, user_id, req.user_id)
    return {"data": {"success": True}}
