from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoUserPalette
from schemas.index import AssoUserPalette, AssoUserPaletteCreate, AssoUserPaletteUpdate
from crud.assouserpalette import create_assouserpalette, get_assouserpalette, update_assouserpalette, delete_assouserpalette  # Importez les fonctions spécifiques

assouserpalette = APIRouter()

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

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
