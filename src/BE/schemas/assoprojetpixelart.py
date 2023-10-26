from pydantic import BaseModel

class AssoProjetPixelArtBase(BaseModel):
    projet_id: int
    pixelart_id: int

class AssoProjetPixelArtCreate(AssoProjetPixelArtBase):
    pass

class AssoProjetPixelArtUpdate(AssoProjetPixelArtBase):
    pass

class AssoProjetPixelArt(AssoProjetPixelArtBase):
    id: int

    class Config:
        orm_mode = True
