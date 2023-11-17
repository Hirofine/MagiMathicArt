from config.db import get_db, Session
from sqlalchemy import text, or_
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import Reponses, AssoUserReponse
from schemas.index import Reponse, ReponseCreate, ReponseUpdate, AssoUserReponseCreate
from crud.reponses import create_reponse, get_reponse, update_reponse, delete_reponse  # Importez les fonctions spécifiques
from crud.assouserreponse import create_assouserreponse

reponse = APIRouter()

@reponse.post("/reponses/", response_model=Reponse)
def rt_create_reponse(reponse: ReponseCreate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        
        reponse_data = dict(reponse)  # Convertit l'objet ReponseCreate en dictionnaire
        rep = create_reponse(db, reponse_data)
        if reponse is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        asso_user_rep = create_assouserreponse(db, dict(user_id = user_id, reponse_id = rep.id))
        if asso_user_rep == None:
            raise HTTPException(status_code=404, detail="Palette not found")

        return rep            

    raise HTTPException(status_code=404, detail="Palette not found")

@reponse.get("/reponses/{reponse_id}", response_model=Reponse)
def rt_read_reponse(reponse_id: int, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        reponse = get_reponse(db, reponse_id)
        if reponse is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        reponse_owner = db.query(AssoUserReponse).filter(reponse.id == AssoUserReponse.reponse_id).first().user_id
        if reponse_owner != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")
            
        return reponse
    raise HTTPException(status_code=404, detail="Palette not found")

@reponse.put("/reponses/{reponse_id}", response_model=Reponse)
def rt_update_reponse(reponse_id: int, reponse: ReponseUpdate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        reponse_db = get_reponse(db, reponse_id)
        if reponse_db is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        reponse_owner = db.query(AssoUserReponse).filter(reponse_db.id == AssoUserReponse.reponse_id).first().user_id
        if reponse_owner != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")
        updated_reponse = update_reponse(db, reponse_id, reponse)
        if updated_reponse is None:
            raise HTTPException(status_code=404, detail="Reponse not found")
        return updated_reponse
    raise HTTPException(status_code=404, detail="Palette not found")

@reponse.delete("/reponses/{reponse_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_reponse(reponse_id: int, db: Session = Depends(get_db)):
    success = delete_reponse(db, reponse_id)
    if not success:
        raise HTTPException(status_code=404, detail="Reponse not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
