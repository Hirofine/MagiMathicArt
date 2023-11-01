from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Couleurs
from schemas.index import Couleur, CouleurCreate, CouleurUpdate
from crud.couleurs import create_couleur, get_couleur, update_couleur, delete_couleur  # Importez les fonctions spécifiques

couleur = APIRouter()

@couleur.post("/couleurs/", response_model=Couleur)
def rt_create_couleur(couleur: CouleurCreate, db: Session = Depends(get_db)):
    couleur_data = dict(couleur)  # Convertit l'objet CouleurCreate en dictionnaire
    return create_couleur(db, couleur_data)

@couleur.get("/couleurs/{couleur_id}", response_model=Couleur)
def rt_read_couleur(couleur_id: int, db: Session = Depends(get_db)):
    couleur = get_couleur(db, couleur_id)
    if couleur is None:
        raise HTTPException(status_code=404, detail="Couleur not found")
    return couleur

@couleur.put("/couleurs/{couleur_id}", response_model=Couleur)
def rt_update_couleur(couleur_id: int, couleur: CouleurUpdate, db: Session = Depends(get_db)):
    updated_couleur = update_couleur(db, couleur_id, couleur)
    if updated_couleur is None:
        raise HTTPException(status_code=404, detail="Couleur not found")
    return updated_couleur

@couleur.delete("/couleurs/{couleur_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_couleur(couleur_id: int, db: Session = Depends(get_db)):
    success = delete_couleur(db, couleur_id)
    if not success:
        raise HTTPException(status_code=404, detail="Couleur not found")
    return None
