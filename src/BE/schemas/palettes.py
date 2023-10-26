from pydantic import BaseModel
from typing import List

class PaletteBase(BaseModel):
    nom: str
    couleurs: List[CouleurCreate]

class PaletteCreate(PaletteBase):
    pass

class PaletteUpdate(PaletteBase):
    pass

class Palette(PaletteBase):
    id: int

    class Config:
        orm_mode = True