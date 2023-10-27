from pydantic import BaseModel

class AssoUserReponseBase(BaseModel):
    user_id:int
    reponse_id: int

class AssoUserReponseCreate(AssoUserReponseBase):
    pass

class AssoUserReponseUpdate(AssoUserReponseBase):
    pass

class AssoUserReponse(AssoUserReponseBase):
    id: int

    class Config:
        orm_mode = True
