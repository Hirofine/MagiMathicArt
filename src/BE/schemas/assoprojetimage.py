from pydantic import BaseModel

class AssoProjetImageBase(BaseModel):
    projet_id: int
    image_id: int
    coordX: int
    coordY: int
    opacite: int
    dimX: int
    dimY: int

class AssoProjetImageCreate(AssoProjetImageBase):
    pass

class AssoProjetImageUpdate(AssoProjetImageBase):
    pass

class AssoProjetImage(AssoProjetImageBase):
    id: int

    class Config:
        orm_mode = True
