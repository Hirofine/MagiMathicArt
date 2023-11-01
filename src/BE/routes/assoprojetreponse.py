from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoProjetReponse
from schemas.index import AssoProjetReponse, AssoProjetReponseCreate, AssoProjetReponseUpdate
from crud.assoprojetreponse import create_assoprojetreponse, get_assoprojetreponse, update_assoprojetreponse, delete_assoprojetreponse  # Importez les fonctions spécifiques

assoprojetreponse = APIRouter()

@assoprojetreponse.post("/assoprojetreponse/", response_model=AssoProjetReponse)
def rt_create_assoprojetreponse(assoprojetreponse: AssoProjetReponseCreate, db: Session = Depends(get_db)):
    assoprojetreponse_data = dict(assoprojetreponse)  # Convertit l'objet AssoProjetReponseCreate en dictionnaire
    return create_assoprojetreponse(db, assoprojetreponse_data)

@assoprojetreponse.get("/assoprojetreponse/{assoprojetreponse_id}", response_model=AssoProjetReponse)
def rt_read_assoprojetreponse(assoprojetreponse_id: int, db: Session = Depends(get_db)):
    assoprojetreponse = get_assoprojetreponse(db, assoprojetreponse_id)
    if assoprojetreponse is None:
        raise HTTPException(status_code=404, detail="AssoProjetReponse not found")
    return assoprojetreponse

@assoprojetreponse.put("/assoprojetreponse/{assoprojetreponse_id}", response_model=AssoProjetReponse)
def rt_update_assoprojetreponse(assoprojetreponse_id: int, assoprojetreponse: AssoProjetReponseUpdate, db: Session = Depends(get_db)):
    updated_assoprojetreponse = update_assoprojetreponse(db, assoprojetreponse_id, assoprojetreponse)
    if updated_assoprojetreponse is None:
        raise HTTPException(status_code=404, detail="AssoProjetReponse not found")
    return updated_assoprojetreponse

@assoprojetreponse.delete("/assoprojetreponse/{assoprojetreponse_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assoprojetreponse(assoprojetreponse_id: int, db: Session = Depends(get_db)):
    success = delete_assoprojetreponse(db, assoprojetreponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoProjetReponse not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
