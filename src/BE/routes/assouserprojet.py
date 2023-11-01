from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoUserProjet
from schemas.index import AssoUserProjet, AssoUserProjetCreate, AssoUserProjetUpdate
from crud.assouserprojet import create_assouserprojet, get_assouserprojet, update_assouserprojet, delete_assouserprojet  # Importez les fonctions spécifiques

assouserprojet = APIRouter()

@assouserprojet.post("/assouserprojet/", response_model=AssoUserProjet)
def rt_create_assouserprojet(assouserprojet: AssoUserProjetCreate, db: Session = Depends(get_db)):
    assouserprojet_data = dict(assouserprojet)  # Convertit l'objet AssoUserProjetCreate en dictionnaire
    return create_assouserprojet(db, assouserprojet_data)

@assouserprojet.get("/assouserprojet/{assouserprojet_id}", response_model=AssoUserProjet)
def rt_read_assouserprojet(assouserprojet_id: int, db: Session = Depends(get_db)):
    assouserprojet = get_assouserprojet(db, assouserprojet_id)
    if assouserprojet is None:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return assouserprojet

@assouserprojet.put("/assouserprojet/{assouserprojet_id}", response_model=AssoUserProjet)
def rt_update_assouserprojet(assouserprojet_id: int, assouserprojet: AssoUserProjetUpdate, db: Session = Depends(get_db)):
    updated_assouserprojet = update_assouserprojet(db, assouserprojet_id, assouserprojet)
    if updated_assouserprojet is None:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return updated_assouserprojet

@assouserprojet.delete("/assouserprojet/{assouserprojet_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserprojet(assouserprojet_id: int, db: Session = Depends(get_db)):
    success = delete_assouserprojet(db, assouserprojet_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
