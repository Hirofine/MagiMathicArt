from pydantic import BaseModel

class AssoProjetPaletteBase(BaseModel):
    projet_id: int
    palette_id: int

class AssoProjetPaletteCreate(AssoProjetPaletteBase):
    pass

class AssoProjetPaletteUpdate(AssoProjetPaletteBase):
    pass

class AssoProjetPalette(AssoProjetPaletteBase):
    id: int

    class Config:
        orm_mode = True
