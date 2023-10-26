from pydantic import BaseModel

class AssoBase(BaseModel):


class AssoCreate(AssoBase):
    pass

class AssoUpdate(AssoBase):
    pass

class Asso(AssoBase):
    id: int

    class Config:
        orm_mode = True
