from pydantic import BaseModel

class ImageBase(BaseModel):
    nom: str
    description: str
    image: bytes

class ImageCreate(ImageBase):
    pass

class ImageUpdate(ImageBase):
    pass

class Image(ImageBase):
    id: int

    class Config:
        orm_mode = True
