from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import PixelArts
from schemas.index import PixelArt, PixelArtCreate, PixelArtUpdate
from crud.pixelarts import create_pixelart, get_pixelart, update_pixelart, delete_pixelart  # Importez les fonctions spécifiques

pixelart = APIRouter()

@pixelart.post("/pixelarts/", response_model=PixelArt)
def rt_create_pixelart(pixelart: PixelArtCreate, db: Session = Depends(get_db)):
    pixelart_data = dict(pixelart)  # Convertit l'objet PixelArtCreate en dictionnaire
    return create_pixelart(db, pixelart_data)

@pixelart.get("/pixelarts/{pixelart_id}", response_model=PixelArt)
def rt_read_pixelart(pixelart_id: int, db: Session = Depends(get_db)):
    pixelart = get_pixelart(db, pixelart_id)
    if pixelart is None:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return pixelart

@pixelart.put("/pixelarts/{pixelart_id}", response_model=PixelArt)
def rt_update_pixelart(pixelart_id: int, pixelart: PixelArtUpdate, db: Session = Depends(get_db)):
    updated_pixelart = update_pixelart(db, pixelart_id, pixelart)
    if updated_pixelart is None:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return updated_pixelart

@pixelart.delete("/pixelarts/{pixelart_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_pixelart(pixelart_id: int, db: Session = Depends(get_db)):
    success = delete_pixelart(db, pixelart_id)
    if not success:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
