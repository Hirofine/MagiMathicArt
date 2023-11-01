from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoProjetImage
from schemas.index import AssoProjetImage, AssoProjetImageCreate, AssoProjetImageUpdate
from crud.assoprojetimage import create_assoprojetimage, get_assoprojetimage, update_assoprojetimage, delete_assoprojetimage  # Importez les fonctions spécifiques

assoprojetimage = APIRouter()

@assoprojetimage.post("/assoprojetimage/", response_model=AssoProjetImage)
def rt_create_assoprojetimage(assoprojetimage: AssoProjetImageCreate, db: Session = Depends(get_db)):
    assoprojetimage_data = dict(assoprojetimage)  # Convertit l'objet AssoProjetImageCreate en dictionnaire
    return create_assoprojetimage(db, assoprojetimage_data)

@assoprojetimage.get("/assoprojetimage/{assoprojetimage_id}", response_model=AssoProjetImage)
def rt_read_assoprojetimage(assoprojetimage_id: int, db: Session = Depends(get_db)):
    assoprojetimage = get_assoprojetimage(db, assoprojetimage_id)
    if assoprojetimage is None:
        raise HTTPException(status_code=404, detail="AssoProjetImage not found")
    return assoprojetimage

@assoprojetimage.put("/assoprojetimage/{assoprojetimage_id}", response_model=AssoProjetImage)
def rt_update_assoprojetimage(assoprojetimage_id: int, assoprojetimage: AssoProjetImageUpdate, db: Session = Depends(get_db)):
    updated_assoprojetimage = update_assoprojetimage(db, assoprojetimage_id, assoprojetimage)
    if updated_assoprojetimage is None:
        raise HTTPException(status_code=404, detail="AssoProjetImage not found")
    return updated_assoprojetimage

@assoprojetimage.delete("/assoprojetimage/{assoprojetimage_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assoprojetimage(assoprojetimage_id: int, db: Session = Depends(get_db)):
    success = delete_assoprojetimage(db, assoprojetimage_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoProjetImage not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
