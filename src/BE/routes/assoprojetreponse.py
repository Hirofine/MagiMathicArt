from config.db import get_db, Session
from sqlalchemy import text, or_
from typing import List
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoProjetReponse as m_AssoProjetReponse, Reponses, Projets, AssoUserProjet, Users
from schemas.index import AssoProjetReponse, AssoProjetReponseCreate, AssoProjetReponseUpdate
from crud.assoprojetreponse import create_assoprojetreponse, get_assoprojetreponse, update_assoprojetreponse, delete_assoprojetreponse  # Importez les fonctions spécifiques
from crud.projets import get_projet
from crud.reponses import get_reponse
assoprojetreponse = APIRouter()

class ReponseCollectionResponse:
    def __init__(self, reponses: List[Reponses]):
        self.reponses = reponses

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

@assoprojetreponse.get("/reponses_from_projet/{projet_id}")
def rt_read_assouserreponse_from_user(projet_id: int, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)

        projet_from_db = db.query(Projets).filter(Projets.id == projet_id).first()
        if projet_from_db == None:
            raise HTTPException(status_code=404, detail="Le projet n'existe pas")


        projet_owner_asso = db.query(AssoUserProjet).filter(AssoUserProjet.projet_id == projet_from_db.id).first()
        if projet_owner_asso == None:
            raise HTTPException(status_code=404, detail="No user registered this project")
        
        projet_owner = db.query(Users).filter(Users.id == projet_owner_asso.user_id).first()
        if projet_owner == None:
            raise HTTPException(status_code=404, detail="L'utilisateur enregistré pour le projet n'existe pas")
        
        if projet_owner.id != user_id:
            raise HTTPException(status_code=404, detail="You are not allowed to access this project")
        
        reponses_from_db = db.query(m_AssoProjetReponse).filter(m_AssoProjetReponse.projet_id == projet_id).all()
        reponse_list = []
        for asso_projet_reponse in reponses_from_db:
            reponse = db.query(Reponses).filter(Reponses.id == asso_projet_reponse.reponse_id).first()
            if reponse:
                reponse_list.append(reponse)
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return ReponseCollectionResponse(reponses=reponse_list)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
