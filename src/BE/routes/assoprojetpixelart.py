from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoProjetPixelArt as m_AssoProjetPixelArt, AssoUserProjet, PixelArts, AssoUserPixelArt
from schemas.index import AssoProjetPixelArt, AssoProjetPixelArtCreate, AssoProjetPixelArtUpdate
from crud.assoprojetpixelart import create_assoprojetpixelart, get_assoprojetpixelart, update_assoprojetpixelart, delete_assoprojetpixelart  # Importez les fonctions spécifiques
from crud.projets import get_projet

assoprojetpixelart = APIRouter()

@assoprojetpixelart.post("/assoprojetpixelart/", response_model=AssoProjetPixelArt)
def rt_create_assoprojetpixelart(assoprojetpixelart: AssoProjetPixelArtCreate, request: Request, db: Session = Depends(get_db)):
    print(assoprojetpixelart)
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet_id = assoprojetpixelart.projet_id
        projet = get_projet(db, projet_id)

        if projet == None:
            print(1)
            raise HTTPException(status_code=404, detail="Ce Projet n'existe pas")

        asso = db.query(AssoUserProjet).filter(AssoUserProjet.user_id == user_id, AssoUserProjet.projet_id == projet_id).first()
        if asso == None:
            print(2)
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à ce projet")

        pixelart = db.query(PixelArts).filter(PixelArts.id == assoprojetpixelart.pixelart_id).first()
        if pixelart == None:
            print(3)
            raise HTTPException(status_code=404, detail="Le pixelart n'existe pas")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(AssoUserPixelArt.user_id == user_id, AssoUserPixelArt.pixelart_id == pixelart.id).first()
        if pixelart_owner == None:
            print(4)
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à ce pixel art")
        
        assoproj_pixart = db.query(m_AssoProjetPixelArt).filter(m_AssoProjetPixelArt.projet_id == projet_id).first()
        if assoproj_pixart != None:
            print(5)
            raise HTTPException(status_code=404, detail="Un pixel Art existe deja pour ce projet")
        
    
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
