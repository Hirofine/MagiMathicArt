from config.db import get_db, Session
from sqlalchemy import text, or_
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoUserReponse as m_AssoUserReponse, Reponses
from schemas.index import AssoUserReponse, AssoUserReponseCreate, AssoUserReponseUpdate
from crud.assouserreponse import create_assouserreponse, get_assouserreponse, update_assouserreponse, delete_assouserreponse  # Importez les fonctions spécifiques

assouserreponse = APIRouter()

class ReponseCollectionResponse:
    def __init__(self, reponses: List[Reponses]):
        self.reponses = reponses

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

@assouserreponse.get("/reponse_from_user/")
def rt_read_assouserreponse_from_user(request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        reponses_from_db = db.query(m_AssoUserReponse).filter(m_AssoUserReponse.user_id == user_id).all()
        reponse_list = []
        for asso_user_reponse in reponses_from_db:
            reponse = db.query(Reponses).filter(Reponses.id == asso_user_reponse.reponse_id).first()
            if reponse:
                reponse_list.append(reponse)
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return ReponseCollectionResponse(reponses=reponse_list)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
