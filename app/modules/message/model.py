from lib2to3.pytree import Base
from typing import Optional
from pydantic import BaseModel


class Message(BaseModel):
    id: Optional[int]
    thread_id: int
    message: str
    user_id: int

    class Config:
        orm_mode = True
