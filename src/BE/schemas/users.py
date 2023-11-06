from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    pseudo: str
    passw: str
    token: Optional[str]
    tokenExpi: Optional[str]
    tokenSalt: Optional[str]

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
