from config.db import get_db, Session
from sqlalchemy import text, or_
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from models.index import AssoUserPalette as m_AssoUserPalette, Palettes
from schemas.index import AssoUserPalette, AssoUserPaletteCreate, AssoUserPaletteUpdate, Palette
from crud.assouserpalette import create_assouserpalette, get_assouserpalette, update_assouserpalette, delete_assouserpalette  # Importez les fonctions spécifiques
from helper import verify_token, user_id_from_token, TOKEN_VALIDE, TOKEN_EXPIRE, TOKEN_INVALIDE, TOKEN_NOT_SENT, USER_NOT_EXISTANT

assouserpalette = APIRouter()

class PaletteCollectionResponse:
    def __init__(self, palettes: List[Palettes]):
        self.palettes = palettes

@assouserpalette.post("/assouserpalette/", response_model=AssoUserPalette)
def rt_create_assouserpalette(assouserpalette: AssoUserPaletteCreate, db: Session = Depends(get_db)):
    assouserpalette_data = dict(assouserpalette)  # Convertit l'objet AssoUserPaletteCreate en dictionnaire
    return create_assouserpalette(db, assouserpalette_data)

@assouserpalette.get("/assouserpalette/{assouserpalette_id}", response_model=AssoUserPalette)
def rt_read_assouserpalette(assouserpalette_id: int, db: Session = Depends(get_db)):
    assouserpalette = get_assouserpalette(db, assouserpalette_id)
    if assouserpalette is None:
        raise HTTPException(status_code=404, detail="AssoUserPalette not found")
    return assouserpalette

@assouserpalette.put("/assouserpalette/{assouserpalette_id}", response_model=AssoUserPalette)
def rt_update_assouserpalette(assouserpalette_id: int, assouserpalette: AssoUserPaletteUpdate, db: Session = Depends(get_db)):
    updated_assouserpalette = update_assouserpalette(db, assouserpalette_id, assouserpalette)
    if updated_assouserpalette is None:
        raise HTTPException(status_code=404, detail="AssoUserPalette not found")
    return updated_assouserpalette

@assouserpalette.delete("/assouserpalette/{assouserpalette_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserpalette(assouserpalette_id: int, db: Session = Depends(get_db)):
    success = delete_assouserpalette(db, assouserpalette_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserPalette not found")
    return None


@assouserpalette.get("/palette_from_user/")
def rt_read_assouserpalette_from_user(request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        palettes_from_db = db.query(m_AssoUserPalette).filter(m_AssoUserPalette.user_id == user_id).all()
        palettes_list = []
        for asso_user_palette in palettes_from_db:
            palette = db.query(Palettes).filter(Palettes.id == asso_user_palette.palette_id).first()
            if palette:
                palettes_list.append(Palettes(id=palette.id, nom=palette.nom))
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return PaletteCollectionResponse(palettes=palettes_list)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
