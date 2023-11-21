from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from typing import List
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoProjetPaletteReponse as m_AssoProjetPaletteReponse, Users, Projets, AssoUserProjet
from schemas.index import AssoProjetPaletteReponse, AssoProjetPaletteReponseCreate, AssoProjetPaletteReponseUpdate
from crud.assoprojetpalettereponse import create_assoprojetpalettereponse, get_assoprojetpalettereponse, update_assoprojetpalettereponse, delete_assoprojetpalettereponse  # Importez les fonctions spécifiques

assoprojetpalettereponse = APIRouter()

class AssoProjetPaletteReponseCollectionResponse:
    def __init__(self, assos: List[m_AssoProjetPaletteReponse]):
        self.assos = assos

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


@assoprojetpalettereponse.get("/assoprojetpalettereponse_from_projet/{projet_id}")
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
        
        assos_from_db = db.query(m_AssoProjetPaletteReponse).filter(m_AssoProjetPaletteReponse.projet_id == projet_id).all()
        
        
        # Retournez la liste d'objets Palettes dans l'objet PaletteCollectionResponse
        return AssoProjetPaletteReponseCollectionResponse(assos=assos_from_db)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")
# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
