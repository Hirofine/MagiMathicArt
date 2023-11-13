from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import PixelArts, AssoUserProjet, AssoProjetPixelArt, AssoUserPixelArt
from schemas.index import PixelArt, PixelArtCreate, PixelArtUpdate
from crud.pixelarts import create_pixelart, get_pixelart, update_pixelart, delete_pixelart  # Importez les fonctions spécifiques
from crud.projets import get_projet

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

@pixelart.get("/pixelart_from_projet/{projet_id}")
def rt_read_palette_full(projet_id: int, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet = get_projet(db, projet_id)
        if projet == None:
            raise HTTPException(status_code=404, detail="Projet not found")
        
        assouserprojet = db.query(AssoUserProjet).filter(AssoUserProjet.projet_id == projet_id).first()
        if assouserprojet == None:
            raise HTTPException(status_code=404, detail="Projet not associated to a user")
        
        if assouserprojet.user_id != user_id:
            raise HTTPException(status_code=404, detail="User not allowed to access")
        
        assoprojetpixelart = db.query(AssoProjetPixelArt).filter(AssoProjetPixelArt.projet_id == projet_id).first()
        if assoprojetpixelart == None:
            raise HTTPException(status_code=404, detail="Pas de pixelart associée à ce projet")

        pixelart_id = assoprojetpixelart.pixelart_id
        pixelart = get_pixelart(db, pixelart_id)
        if pixelart is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(pixelart_id == AssoUserPixelArt.pixelart_id).first()

        if pixelart_owner == None:
            raise HTTPException(status_code=404, detail="Pas d'utilisateur associé à ce pixel_art")
        
        if pixelart_owner.user_id != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à ce pixelart")

        return pixelart
    else :
        raise HTTPException(status_code=404, detail="Palette not found")

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
