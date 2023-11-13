from config.db import get_db, Session
from sqlalchemy import text, or_
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoUserProjet as m_AssoUserProjet, Projets
from schemas.index import AssoUserProjet, AssoUserProjetCreate, AssoUserProjetUpdate
from crud.assouserprojet import create_assouserprojet, get_assouserprojet, update_assouserprojet, delete_assouserprojet  # Importez les fonctions spécifiques

assouserprojet = APIRouter()

class ProjetsCollectionResponse:
    def __init__(self, projets: List[Projets]):
        self.projets = projets

@assouserprojet.post("/assouserprojet/", response_model=AssoUserProjet)
def rt_create_assouserprojet(assouserprojet: AssoUserProjetCreate, db: Session = Depends(get_db)):
    assouserprojet_data = dict(assouserprojet)  # Convertit l'objet AssoUserProjetCreate en dictionnaire
    return create_assouserprojet(db, assouserprojet_data)

@assouserprojet.get("/assouserprojet/{assouserprojet_id}", response_model=AssoUserProjet)
def rt_read_assouserprojet(assouserprojet_id: int, db: Session = Depends(get_db)):
    assouserprojet = get_assouserprojet(db, assouserprojet_id)
    if assouserprojet is None:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return assouserprojet

@assouserprojet.put("/assouserprojet/{assouserprojet_id}", response_model=AssoUserProjet)
def rt_update_assouserprojet(assouserprojet_id: int, assouserprojet: AssoUserProjetUpdate, db: Session = Depends(get_db)):
    updated_assouserprojet = update_assouserprojet(db, assouserprojet_id, assouserprojet)
    if updated_assouserprojet is None:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return updated_assouserprojet

@assouserprojet.delete("/assouserprojet/{assouserprojet_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_assouserprojet(assouserprojet_id: int, db: Session = Depends(get_db)):
    success = delete_assouserprojet(db, assouserprojet_id)
    if not success:
        raise HTTPException(status_code=404, detail="AssoUserProjet not found")
    return None

@assouserprojet.get("/projet_from_user/")
def rt_read_assouserprojet_from_user(request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projets_from_db = db.query(m_AssoUserProjet).filter(m_AssoUserProjet.user_id == user_id).all()
        projets_list = []
        for asso_user_projet in projets_from_db:
            projet = db.query(Projets).filter(Projets.id == asso_user_projet.projet_id).first()
            if projet:
                projets_list.append(Projets(id=projet.id, nom=projet.nom))
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return ProjetsCollectionResponse(projets=projets_list)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
