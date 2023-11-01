from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Palettes
from schemas.index import Palette, PaletteCreate, PaletteUpdate
from crud.palettes import create_palette, get_palette, update_palette, delete_palette  # Importez les fonctions spécifiques

palette = APIRouter()

@palette.post("/palettes/", response_model=Palette)
def rt_create_palette(palette: PaletteCreate, db: Session = Depends(get_db)):
    palette_data = dict(palette)  # Convertit l'objet PaletteCreate en dictionnaire
    return create_palette(db, palette_data)

@palette.get("/palettes/{palette_id}", response_model=Palette)
def rt_read_palette(palette_id: int, db: Session = Depends(get_db)):
    palette = get_palette(db, palette_id)
    if palette is None:
        raise HTTPException(status_code=404, detail="Palette not found")
    return palette

@palette.put("/palettes/{palette_id}", response_model=Palette)
def rt_update_palette(palette_id: int, palette: PaletteUpdate, db: Session = Depends(get_db)):
    updated_palette = update_palette(db, palette_id, palette)
    if updated_palette is None:
        raise HTTPException(status_code=404, detail="Palette not found")
    return updated_palette

@palette.delete("/palettes/{palette_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_palette(palette_id: int, db: Session = Depends(get_db)):
    success = delete_palette(db, palette_id)
    if not success:
        raise HTTPException(status_code=404, detail="Palette not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
