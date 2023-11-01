from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Reponses
from schemas.index import Reponse, ReponseCreate, ReponseUpdate
from crud.reponses import create_reponse, get_reponse, update_reponse, delete_reponse  # Importez les fonctions spécifiques

reponse = APIRouter()

@reponse.post("/reponses/", response_model=Reponse)
def rt_create_reponse(reponse: ReponseCreate, db: Session = Depends(get_db)):
    reponse_data = dict(reponse)  # Convertit l'objet ReponseCreate en dictionnaire
    return create_reponse(db, reponse_data)

@reponse.get("/reponses/{reponse_id}", response_model=Reponse)
def rt_read_reponse(reponse_id: int, db: Session = Depends(get_db)):
    reponse = get_reponse(db, reponse_id)
    if reponse is None:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return reponse

@reponse.put("/reponses/{reponse_id}", response_model=Reponse)
def rt_update_reponse(reponse_id: int, reponse: ReponseUpdate, db: Session = Depends(get_db)):
    updated_reponse = update_reponse(db, reponse_id, reponse)
    if updated_reponse is None:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return updated_reponse

@reponse.delete("/reponses/{reponse_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_reponse(reponse_id: int, db: Session = Depends(get_db)):
    success = delete_reponse(db, reponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
