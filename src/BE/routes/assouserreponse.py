from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoUserReponse
from schemas.index import AssoUserReponse, AssoUserReponseCreate, AssoUserReponseUpdate
from crud.assouserreponse import create_assouserreponse, get_assouserreponse, update_assouserreponse, delete_assouserreponse  # Importez les fonctions spécifiques

assouserreponse = APIRouter()

@assouserreponse.post("/assouserreponse/", response_model=AssoUserReponse)
def rt_create_assouserreponse(assouserreponse: AssoUserReponseCreate, db: Session = Depends(get_db)):
    assouserreponse_data = dict(assouserreponse)  # Convertit l'objet AssoUserReponseCreate en dictionnaire
    return create_assouserreponse(db, assouserreponse_data)

@assouserreponse.get("/assouserreponse/{assouserreponse_id}", response_model=AssoUserReponse)
def rt_read_assouserreponse(assouserreponse_id: int, db: Session = Depends(get_db)):
    assouserreponse = get_assouserreponse(db, assouserreponse_id)
    if assouserreponse is None:
        raise HTTPException(status_code=404, detail="AssoUserReponse not found")
    return assouserreponse

@assouserreponse.put("/assouserreponse/{assouserreponse_id}", response_model=AssoUserReponse)
def rt_update_assouserreponse(assouserreponse_id: int, assouserreponse: AssoUserReponseUpdate, db: Session = Depends(get_db)):
    updated_assouserreponse = update_assouserreponse(db, assouserreponse_id, assouserreponse)
    if updated_assouserreponse is None:
        raise HTTPException(status_code=404, detail="AssoUserReponse not found")
    return updated_assouserreponse

@assouserreponse.delete("/assouserreponse/{assouserreponse_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserreponse(assouserreponse_id: int, db: Session = Depends(get_db)):
    success = delete_assouserreponse(db, assouserreponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserReponse not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
