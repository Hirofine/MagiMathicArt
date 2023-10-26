from pydantic import BaseModel

class ReponseBase(BaseModel):
    nom: str
    description: str
    fonction: str

class ReponseCreate(ReponseBase):
    pass

class ReponseUpdate(ReponseBase):
    pass

class Reponse(ReponseBase):
    id: int

    class Config:
        orm_mode = True
