from config.db import get_db, Session
from typing import List
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoUserPixelArt as m_AssoUserPixelArt, PixelArts
from schemas.index import AssoUserPixelArt, AssoUserPixelArtCreate, AssoUserPixelArtUpdate
from crud.assouserpixelart import create_assouserpixelart, get_assouserpixelart, update_assouserpixelart, delete_assouserpixelart  # Importez les fonctions spécifiques

assouserpixelart = APIRouter()

class PixelArtCollectionResponse:
    def __init__(self, pixelarts: List[PixelArts]):
        self.pixelarts = pixelarts

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

@assouserpixelart.get("/pixel_art_from_user/")
def rt_read_assouserpixelart_from_user(request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        pixelarts_from_db = db.query(m_AssoUserPixelArt).filter(m_AssoUserPixelArt.user_id == user_id).all()
        pixelarts_list = []
        for asso_user_pixel_art in pixelarts_from_db:
            pixel_art = db.query(PixelArts).filter(PixelArts.id == asso_user_pixel_art.pixelart_id).first()
            if pixel_art:
                pixelarts_list.append(PixelArts(id=pixel_art.id, nom=pixel_art.nom))
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return PixelArtCollectionResponse(pixelarts=pixelarts_list)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
