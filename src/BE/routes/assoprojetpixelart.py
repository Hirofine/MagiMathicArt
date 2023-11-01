from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoProjetPixelArt
from schemas.index import AssoProjetPixelArt, AssoProjetPixelArtCreate, AssoProjetPixelArtUpdate
from crud.assoprojetpixelart import create_assoprojetpixelart, get_assoprojetpixelart, update_assoprojetpixelart, delete_assoprojetpixelart  # Importez les fonctions spécifiques

assoprojetpixelart = APIRouter()

@assoprojetpixelart.post("/assoprojetpixelart/", response_model=AssoProjetPixelArt)
def rt_create_assoprojetpixelart(assoprojetpixelart: AssoProjetPixelArtCreate, db: Session = Depends(get_db)):
    assoprojetpixelart_data = dict(assoprojetpixelart)  # Convertit l'objet AssoProjetPixelArtCreate en dictionnaire
    return create_assoprojetpixelart(db, assoprojetpixelart_data)

@assoprojetpixelart.get("/assoprojetpixelart/{assoprojetpixelart_id}", response_model=AssoProjetPixelArt)
def rt_read_assoprojetpixelart(assoprojetpixelart_id: int, db: Session = Depends(get_db)):
    assoprojetpixelart = get_assoprojetpixelart(db, assoprojetpixelart_id)
    if assoprojetpixelart is None:
        raise HTTPException(status_code=404, detail="AssoProjetPixelArt not found")
    return assoprojetpixelart

@assoprojetpixelart.put("/assoprojetpixelart/{assoprojetpixelart_id}", response_model=AssoProjetPixelArt)
def rt_update_assoprojetpixelart(assoprojetpixelart_id: int, assoprojetpixelart: AssoProjetPixelArtUpdate, db: Session = Depends(get_db)):
    updated_assoprojetpixelart = update_assoprojetpixelart(db, assoprojetpixelart_id, assoprojetpixelart)
    if updated_assoprojetpixelart is None:
        raise HTTPException(status_code=404, detail="AssoProjetPixelArt not found")
    return updated_assoprojetpixelart

@assoprojetpixelart.delete("/assoprojetpixelart/{assoprojetpixelart_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assoprojetpixelart(assoprojetpixelart_id: int, db: Session = Depends(get_db)):
    success = delete_assoprojetpixelart(db, assoprojetpixelart_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoProjetPixelArt not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
