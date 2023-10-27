from pydantic import BaseModel

class ProjetBase(BaseModel):
    id: int
    nom: str
    description: str
    user_id: int

class ProjetCreate(ProjetBase):
    pass

class ProjetUpdate(ProjetBase):
    pass

class Projet(ProjetBase):
    id: int

    class Config:
        orm_mode = True
