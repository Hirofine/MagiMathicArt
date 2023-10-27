from pydantic import BaseModel

class AssoUserProjetBase(BaseModel):
    user_id: int
    projet_id: int

class AssoUserProjetCreate(AssoUserProjetBase):
    pass

class AssoUserProjetUpdate(AssoUserProjetBase):
    pass

class AssoUserProjet(AssoUserProjetBase):
    id: int

    class Config:
        orm_mode = True
