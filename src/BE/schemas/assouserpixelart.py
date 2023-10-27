from pydantic import BaseModel

class AssoUserPixelArtBase(BaseModel):
    user_id: int
    pixelart_id: int

class AssoUserPixelArtCreate(AssoUserPixelArtBase):
    pass

class AssoUserPixelArtUpdate(AssoUserPixelArtBase):
    pass

class AssoUserPixelArt(AssoUserPixelArtBase):
    id: int

    class Config:
        orm_mode = True
