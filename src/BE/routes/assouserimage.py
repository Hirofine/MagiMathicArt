from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import AssoUserImage
from schemas.index import AssoUserImage, AssoUserImageCreate, AssoUserImageUpdate
from crud.assouserimage import create_assouserimage, get_assouserimage, update_assouserimage, delete_assouserimage  # Importez les fonctions spécifiques

assouserimage = APIRouter()

@assouserimage.post("/assouserimage/", response_model=AssoUserImage)
def rt_create_assouserimage(assouserimage: AssoUserImageCreate, db: Session = Depends(get_db)):
    assouserimage_data = dict(assouserimage)  # Convertit l'objet AssoUserImageCreate en dictionnaire
    return create_assouserimage(db, assouserimage_data)

@assouserimage.get("/assouserimage/{assouserimage_id}", response_model=AssoUserImage)
def rt_read_assouserimage(assouserimage_id: int, db: Session = Depends(get_db)):
    assouserimage = get_assouserimage(db, assouserimage_id)
    if assouserimage is None:
        raise HTTPException(status_code=404, detail="AssoUserImage not found")
    return assouserimage

@assouserimage.put("/assouserimage/{assouserimage_id}", response_model=AssoUserImage)
def rt_update_assouserimage(assouserimage_id: int, assouserimage: AssoUserImageUpdate, db: Session = Depends(get_db)):
    updated_assouserimage = update_assouserimage(db, assouserimage_id, assouserimage)
    if updated_assouserimage is None:
        raise HTTPException(status_code=404, detail="AssoUserImage not found")
    return updated_assouserimage

@assouserimage.delete("/assouserimage/{assouserimage_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserimage(assouserimage_id: int, db: Session = Depends(get_db)):
    success = delete_assouserimage(db, assouserimage_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserImage not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
