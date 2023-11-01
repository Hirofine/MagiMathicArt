from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Images
from schemas.index import Image, ImageCreate, ImageUpdate
from crud.images import create_image, get_image, update_image, delete_image  # Importez les fonctions spécifiques

image = APIRouter()

@image.post("/images/", response_model=Image)
def rt_create_image(image: ImageCreate, db: Session = Depends(get_db)):
    image_data = dict(image)  # Convertit l'objet ImageCreate en dictionnaire
    return create_image(db, image_data)

@image.get("/images/{image_id}", response_model=Image)
def rt_read_image(image_id: int, db: Session = Depends(get_db)):
    image = get_image(db, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return image

@image.put("/images/{image_id}", response_model=Image)
def rt_update_image(image_id: int, image: ImageUpdate, db: Session = Depends(get_db)):
    updated_image = update_image(db, image_id, image)
    if updated_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    return updated_image

@image.delete("/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_image(image_id: int, db: Session = Depends(get_db)):
    success = delete_image(db, image_id)
    if not success:
        raise HTTPException(status_code=404, detail="Image not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
