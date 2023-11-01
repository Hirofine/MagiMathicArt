from pydantic import BaseModel

class ProjetBase(BaseModel):
    nom: str
    description: str

class ProjetCreate(ProjetBase):
    pass

class ProjetUpdate(ProjetBase):
    pass

class Projet(ProjetBase):
    id: int

    class Config:
        orm_mode = True
