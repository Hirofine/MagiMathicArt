from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoProjetPalette as m_AssoProjetPalette, AssoUserProjet, Palettes, AssoUserPalette
from schemas.index import AssoProjetPalette, AssoProjetPaletteCreate, AssoProjetPaletteUpdate
from crud.assoprojetpalette import create_assoprojetpalette, get_assoprojetpalette, update_assoprojetpalette, delete_assoprojetpalette  # Importez les fonctions spécifiques
from crud.projets import get_projet
from crud.assouserprojet import get_assouserprojet

assoprojetpalette = APIRouter()

@assoprojetpalette.post("/assoprojetpalette/", response_model=AssoProjetPalette)
def rt_create_assoprojetpalette(assoprojetpalette: AssoProjetPaletteCreate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet_id = assoprojetpalette.projet_id
        projet = get_projet(db, projet_id)

        if projet == None:
            raise HTTPException(status_code=404, detail="Ce Projet n'existe pas")

        asso = db.query(AssoUserProjet).filter(AssoUserProjet.user_id == user_id, AssoUserProjet.projet_id == projet_id).first()
        if asso == None:
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à ce projet")

        palette = db.query(Palettes).filter(Palettes.id == assoprojetpalette.palette_id).first()
        if palette == None:
            raise HTTPException(status_code=404, detail="La palette n'existe pas")

        assopal = db.query(AssoUserPalette).filter(AssoUserPalette.user_id == user_id, AssoUserPalette.palette_id == palette.id).first()
        if assopal == None:
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à cette palette")
        
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

@assoprojetpalette.put("/assoprojetpalette_from_projet/{projet_id}", response_model=AssoProjetPalette)
def rt_update_assoprojetpalette(projet_id: int, assoprojetpalette: AssoProjetPaletteUpdate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet = get_projet(db, projet_id)

        if projet == None:
            raise HTTPException(status_code=404, detail="Ce Projet n'existe pas")

        asso = db.query(AssoUserProjet).filter(AssoUserProjet.user_id == user_id, AssoUserProjet.projet_id == projet_id).first()
        if asso == None:
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à ce projet")

        palette = db.query(Palettes).filter(Palettes.id == assoprojetpalette.palette_id).first()
        if palette == None:
            raise HTTPException(status_code=404, detail="La palette n'existe pas")

        assopal = db.query(AssoUserPalette).filter(AssoUserPalette.user_id == user_id, AssoUserPalette.palette_id == palette.id).first()
        if assopal == None:
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à cette palette")
        
        assoprojpal = db.query(m_AssoProjetPalette).filter(m_AssoProjetPalette.projet_id == projet_id).first()
        if assoprojpal == None:
            raise HTTPException(status_code=404, detail="Aucune palette associée à ce projet")
        
        updated_assoprojetpalette = update_assoprojetpalette(db, assoprojpal.id, assoprojetpalette)
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
