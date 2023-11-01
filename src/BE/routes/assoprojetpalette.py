from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoProjetPalette
from schemas.index import AssoProjetPalette, AssoProjetPaletteCreate, AssoProjetPaletteUpdate
from crud.assoprojetpalette import create_assoprojetpalette, get_assoprojetpalette, update_assoprojetpalette, delete_assoprojetpalette  # Importez les fonctions spécifiques

assoprojetpalette = APIRouter()

@assoprojetpalette.post("/assoprojetpalette/", response_model=AssoProjetPalette)
def rt_create_assoprojetpalette(assoprojetpalette: AssoProjetPaletteCreate, db: Session = Depends(get_db)):
    assoprojetpalette_data = dict(assoprojetpalette)  # Convertit l'objet AssoProjetPaletteCreate en dictionnaire
    return create_assoprojetpalette(db, assoprojetpalette_data)

@assoprojetpalette.get("/assoprojetpalette/{assoprojetpalette_id}", response_model=AssoProjetPalette)
def rt_read_assoprojetpalette(assoprojetpalette_id: int, db: Session = Depends(get_db)):
    assoprojetpalette = get_assoprojetpalette(db, assoprojetpalette_id)
    if assoprojetpalette is None:
        raise HTTPException(status_code=404, detail="AssoProjetPalette not found")
    return assoprojetpalette

@assoprojetpalette.put("/assoprojetpalette/{assoprojetpalette_id}", response_model=AssoProjetPalette)
def rt_update_assoprojetpalette(assoprojetpalette_id: int, assoprojetpalette: AssoProjetPaletteUpdate, db: Session = Depends(get_db)):
    updated_assoprojetpalette = update_assoprojetpalette(db, assoprojetpalette_id, assoprojetpalette)
    if updated_assoprojetpalette is None:
        raise HTTPException(status_code=404, detail="AssoProjetPalette not found")
    return updated_assoprojetpalette

@assoprojetpalette.delete("/assoprojetpalette/{assoprojetpalette_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assoprojetpalette(assoprojetpalette_id: int, db: Session = Depends(get_db)):
    success = delete_assoprojetpalette(db, assoprojetpalette_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoProjetPalette not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
