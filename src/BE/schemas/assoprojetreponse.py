from pydantic import BaseModel

class AssoProjetReponseBase(BaseModel):
    projet_id: int
    reponse_id: int

class AssoProjetReponseCreate(AssoProjetReponseBase):
    pass

class AssoProjetReponseUpdate(AssoProjetReponseBase):
    pass

class AssoProjetReponse(AssoProjetReponseBase):
    id: int

    class Config:
        orm_mode = True
