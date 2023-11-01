from pydantic import BaseModel
from typing import List
from .couleurs import Couleur, CouleurBase, CouleurCreate, CouleurUpdate

class PaletteBase(BaseModel):
    nom: str

class PaletteCreate(PaletteBase):
    pass

class PaletteUpdate(PaletteBase):
    pass

class Palette(PaletteBase):
    id: int

    class Config:
        orm_mode = True
