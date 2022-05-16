from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id: Optional[int]
    username: str
    password: str

    class Config:
        orm_mode = True
