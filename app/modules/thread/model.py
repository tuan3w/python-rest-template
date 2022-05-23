from typing import Optional

from pydantic import BaseModel


class ChatThread(BaseModel):
    id: Optional[int]
    owner_id: int
    name: str

    class Config:
        orm_mode = True


class ChatThreadMember(BaseModel):
    id: Optional[int]
    thread_id: int
    user_id: int
    role: str = "member"

    class Config:
        orm_mode = True
