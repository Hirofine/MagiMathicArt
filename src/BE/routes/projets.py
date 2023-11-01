from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Projets
from schemas.index import Projet, ProjetCreate, ProjetUpdate
from crud.projets import create_projet, get_projet, update_projet, delete_projet  # Importez les fonctions spécifiques

projet = APIRouter()

@projet.post("/projets/", response_model=Projet)
def rt_create_projet(projet: ProjetCreate, db: Session = Depends(get_db)):
    projet_data = dict(projet)  # Convertit l'objet ProjetCreate en dictionnaire
    return create_projet(db, projet_data)

@projet.get("/projets/{projet_id}", response_model=Projet)
def rt_read_projet(projet_id: int, db: Session = Depends(get_db)):
    projet = get_projet(db, projet_id)
    if projet is None:
        raise HTTPException(status_code=404, detail="Projet not found")
    return projet

@projet.put("/projets/{projet_id}", response_model=Projet)
def rt_update_projet(projet_id: int, projet: ProjetUpdate, db: Session = Depends(get_db)):
    updated_projet = update_projet(db, projet_id, projet)
    if updated_projet is None:
        raise HTTPException(status_code=404, detail="Projet not found")
    return updated_projet

@projet.delete("/projets/{projet_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_projet(projet_id: int, db: Session = Depends(get_db)):
    success = delete_projet(db, projet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Projet not found")
    return None
