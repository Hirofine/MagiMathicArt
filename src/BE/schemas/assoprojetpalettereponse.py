from pydantic import BaseModel

class AssoProjetPaletteReponseBase(BaseModel):
    projet_id: int
    palette_id: int
    reponse_id: int
    position: int

class AssoProjetPaletteReponseCreate(AssoProjetPaletteReponseBase):
    pass

class AssoProjetPaletteReponseUpdate(AssoProjetPaletteReponseBase):
    pass

class AssoProjetPaletteReponse(AssoProjetPaletteReponseBase):
    id: int

    class Config:
        orm_mode = True
