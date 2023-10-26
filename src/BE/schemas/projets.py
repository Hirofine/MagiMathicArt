from pydantic import BaseModel

class CouleurBase(BaseModel):
    color: str

class CouleurCreate(CouleurBase):
    pass

class CouleurUpdate(CouleurBase):
    pass

class Couleur(CouleurBase):
    id: int

    class Config:
        orm_mode = True
