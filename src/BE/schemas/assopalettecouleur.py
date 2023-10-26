from pydantic import BaseModel

class AssoPaletteCouleurBase(BaseModel):
    palette_id: int
    couleur_id: int
    position: int

class AssoPaletteCouleurCreate(AssoPaletteCouleurBase):
    pass

class AssoPaletteCouleurUpdate(AssoPaletteCouleurBase):
    pass

class AssoPaletteCouleur(AssoPaletteCouleurBase):
    id: int

    class Config:
        orm_mode = True
