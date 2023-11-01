from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoUserPixelArt
from schemas.index import AssoUserPixelArt, AssoUserPixelArtCreate, AssoUserPixelArtUpdate
from crud.assouserpixelart import create_assouserpixelart, get_assouserpixelart, update_assouserpixelart, delete_assouserpixelart  # Importez les fonctions spécifiques

assouserpixelart = APIRouter()

@assouserpixelart.post("/assouserpixelart/", response_model=AssoUserPixelArt)
def rt_create_assouserpixelart(assouserpixelart: AssoUserPixelArtCreate, db: Session = Depends(get_db)):
    assouserpixelart_data = dict(assouserpixelart)  # Convertit l'objet AssoUserPixelArtCreate en dictionnaire
    return create_assouserpixelart(db, assouserpixelart_data)

@assouserpixelart.get("/assouserpixelart/{assouserpixelart_id}", response_model=AssoUserPixelArt)
def rt_read_assouserpixelart(assouserpixelart_id: int, db: Session = Depends(get_db)):
    assouserpixelart = get_assouserpixelart(db, assouserpixelart_id)
    if assouserpixelart is None:
        raise HTTPException(status_code=404, detail="AssoUserPixelArt not found")
    return assouserpixelart

@assouserpixelart.put("/assouserpixelart/{assouserpixelart_id}", response_model=AssoUserPixelArt)
def rt_update_assouserpixelart(assouserpixelart_id: int, assouserpixelart: AssoUserPixelArtUpdate, db: Session = Depends(get_db)):
    updated_assouserpixelart = update_assouserpixelart(db, assouserpixelart_id, assouserpixelart)
    if updated_assouserpixelart is None:
        raise HTTPException(status_code=404, detail="AssoUserPixelArt not found")
    return updated_assouserpixelart

@assouserpixelart.delete("/assouserpixelart/{assouserpixelart_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserpixelart(assouserpixelart_id: int, db: Session = Depends(get_db)):
    success = delete_assouserpixelart(db, assouserpixelart_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserPixelArt not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
