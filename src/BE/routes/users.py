from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status
from fastapi.responses import StreamingResponse
from models.index import Users
from schemas.index import User, UserCreate, UserUpdate
from crud.users import create_user, get_user, update_user, delete_user  # Importez les fonctions spécifiques

user = APIRouter()

@user.post("/users/", response_model=User)
def rt_create_user(user: UserCreate, db: Session = Depends(get_db)):
    user_data = dict(user)  # Convertit l'objet UserCreate en dictionnaire
    return create_user(db, user_data)

@user.get("/users/{user_id}", response_model=User)
def rt_read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.put("/users/{user_id}", response_model=User)
def rt_update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user(db, user_id, user)
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@user.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_user(user_id: int, db: Session = Depends(get_db)):
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
