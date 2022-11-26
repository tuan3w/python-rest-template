from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    id: Optional[int] = None
    username: str
    password: str


class User(UserCreate):
    id: int

    class Config:
        orm_mode = True
