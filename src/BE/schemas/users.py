from pydantic import BaseModel

class UserBase(BaseModel):
    pseudo: str
    passw: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
