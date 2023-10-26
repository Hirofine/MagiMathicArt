from pydantic import BaseModel

class PixelArtBase(BaseModel):
    nom: str
    description: str
    dimensionsX: int
    dimensionsY: int
    art: str

class PixelArtCreate(PixelArtBase):
    pass

class PixelArtUpdate(PixelArtBase):
    pass

class PixelArt(PixelArtBase):
    id: int

    class Config:
        orm_mode = True
