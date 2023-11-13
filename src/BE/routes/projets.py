from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import Projets, AssoUserProjet
from schemas.index import Projet, ProjetCreate, ProjetUpdate, AssoUserProjetCreate
from crud.projets import create_projet, get_projet, update_projet, delete_projet  # Importez les fonctions spécifiques
from crud.assouserprojet import create_assouserprojet

projet = APIRouter()

@projet.post("/projets/", response_model=Projet)
def rt_create_projet(projet: ProjetCreate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet_data = dict(projet)  # Convertit l'objet ProjetCreate en dictionnaire
        proj = create_projet(db, projet_data)
        asso = create_assouserprojet(db, dict(AssoUserProjetCreate(user_id = user_id, projet_id = proj.id)))
    return proj

@projet.get("/projets/{projet_id}", response_model=Projet)
def rt_read_projet(projet_id: int, request: Request,  db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        
        projet = get_projet(db, projet_id)
        if projet is None:
            raise HTTPException(status_code=404, detail="Projet not found")
        asso = db.query(AssoUserProjet).filter(AssoUserProjet.user_id == user_id, AssoUserProjet.projet_id == projet_id).first()
        if asso == None:
            raise HTTPException(status_code=404, detail="Vous n'avez pas acces à ce projet")
        return projet
    return HTTPException(status_code=404, detail="Vous n'etes pas identifié")

@projet.put("/projets/{projet_id}", response_model=Projet)
def rt_update_projet(projet_id: int, projet: ProjetUpdate, db: Session = Depends(get_db)):
    updated_projet = update_projet(db, projet_id, projet)
    if updated_projet is None:
        raise HTTPException(status_code=404, detail="Projet not found")
    return updated_projet

@projet.delete("/projets/{projet_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_projet(projet_id: int, db: Session = Depends(get_db)):
    success = delete_projet(db, projet_id)
    if not success:
        raise HTTPException(status_code=404, detail="Projet not found")
    return None
