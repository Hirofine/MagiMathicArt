from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoPaletteCouleur
from schemas.index import AssoPaletteCouleur, AssoPaletteCouleurCreate, AssoPaletteCouleurUpdate
from crud.assopalettecouleur import create_assopalettecouleur, get_assopalettecouleur, update_assopalettecouleur, delete_assopalettecouleur  # Importez les fonctions spécifiques

assopalettecouleur = APIRouter()

@assopalettecouleur.post("/assopalettecouleur/", response_model=AssoPaletteCouleur)
def rt_create_assopalettecouleur(assopalettecouleur: AssoPaletteCouleurCreate, db: Session = Depends(get_db)):
    assopalettecouleur_data = dict(assopalettecouleur)  # Convertit l'objet AssoPaletteCouleurCreate en dictionnaire
    return create_assopalettecouleur(db, assopalettecouleur_data)

@assopalettecouleur.get("/assopalettecouleur/{assopalettecouleur_id}", response_model=AssoPaletteCouleur)
def rt_read_assopalettecouleur(assopalettecouleur_id: int, db: Session = Depends(get_db)):
    assopalettecouleur = get_assopalettecouleur(db, assopalettecouleur_id)
    if assopalettecouleur is None:
        raise HTTPException(status_code=404, detail="AssoPaletteCouleur not found")
    return assopalettecouleur

@assopalettecouleur.put("/assopalettecouleur/{assopalettecouleur_id}", response_model=AssoPaletteCouleur)
def rt_update_assopalettecouleur(assopalettecouleur_id: int, assopalettecouleur: AssoPaletteCouleurUpdate, db: Session = Depends(get_db)):
    updated_assopalettecouleur = update_assopalettecouleur(db, assopalettecouleur_id, assopalettecouleur)
    if updated_assopalettecouleur is None:
        raise HTTPException(status_code=404, detail="AssoPaletteCouleur not found")
    return updated_assopalettecouleur

@assopalettecouleur.delete("/assopalettecouleur/{assopalettecouleur_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assopalettecouleur(assopalettecouleur_id: int, db: Session = Depends(get_db)):
    success = delete_assopalettecouleur(db, assopalettecouleur_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoPaletteCouleur not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
