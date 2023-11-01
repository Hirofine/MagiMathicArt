from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoProjetPaletteReponse
from schemas.index import AssoProjetPaletteReponse, AssoProjetPaletteReponseCreate, AssoProjetPaletteReponseUpdate
from crud.assoprojetpalettereponse import create_assoprojetpalettereponse, get_assoprojetpalettereponse, update_assoprojetpalettereponse, delete_assoprojetpalettereponse  # Importez les fonctions spécifiques

assoprojetpalettereponse = APIRouter()

@assoprojetpalettereponse.post("/assoprojetpalettereponse/", response_model=AssoProjetPaletteReponse)
def rt_create_assoprojetpalettereponse(assoprojetpalettereponse: AssoProjetPaletteReponseCreate, db: Session = Depends(get_db)):
    assoprojetpalettereponse_data = dict(assoprojetpalettereponse)  # Convertit l'objet AssoProjetPaletteReponseCreate en dictionnaire
    return create_assoprojetpalettereponse(db, assoprojetpalettereponse_data)

@assoprojetpalettereponse.get("/assoprojetpalettereponse/{assoprojetpalettereponse_id}", response_model=AssoProjetPaletteReponse)
def rt_read_assoprojetpalettereponse(assoprojetpalettereponse_id: int, db: Session = Depends(get_db)):
    assoprojetpalettereponse = get_assoprojetpalettereponse(db, assoprojetpalettereponse_id)
    if assoprojetpalettereponse is None:
        raise HTTPException(status_code=404, detail="AssoProjetPaletteReponse not found")
    return assoprojetpalettereponse

@assoprojetpalettereponse.put("/assoprojetpalettereponse/{assoprojetpalettereponse_id}", response_model=AssoProjetPaletteReponse)
def rt_update_assoprojetpalettereponse(assoprojetpalettereponse_id: int, assoprojetpalettereponse: AssoProjetPaletteReponseUpdate, db: Session = Depends(get_db)):
    updated_assoprojetpalettereponse = update_assoprojetpalettereponse(db, assoprojetpalettereponse_id, assoprojetpalettereponse)
    if updated_assoprojetpalettereponse is None:
        raise HTTPException(status_code=404, detail="AssoProjetPaletteReponse not found")
    return updated_assoprojetpalettereponse

@assoprojetpalettereponse.delete("/assoprojetpalettereponse/{assoprojetpalettereponse_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assoprojetpalettereponse(assoprojetpalettereponse_id: int, db: Session = Depends(get_db)):
    success = delete_assoprojetpalettereponse(db, assoprojetpalettereponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoProjetPaletteReponse not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
