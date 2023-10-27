from pydantic import BaseModel

class AssoUserPaletteBase(BaseModel):
    user_id: int
    palette_id: int

class AssoUserPaletteCreate(AssoUserPaletteBase):
    pass

class AssoUserPaletteUpdate(AssoUserPaletteBase):
    pass

class AssoUserPalette(AssoUserPaletteBase):
    id: int

    class Config:
        orm_mode = True
