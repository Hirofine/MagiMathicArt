from config.db import get_db, Session
from sqlalchemy import text, or_
from pydantic import BaseModel
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from typing import List
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import AssoProjetPaletteReponse as m_AssoProjetPaletteReponse, Users, Projets, AssoUserProjet, Palettes, AssoProjetPalette, AssoUserPalette, AssoUserReponse, Reponses, AssoProjetReponse
from schemas.index import AssoProjetPaletteReponse, AssoProjetPaletteReponseCreate, AssoProjetPaletteReponseUpdate
from crud.assoprojetpalettereponse import create_assoprojetpalettereponse, get_assoprojetpalettereponse, update_assoprojetpalettereponse, delete_assoprojetpalettereponse  # Importez les fonctions spécifiques
from crud.assoprojetreponse import create_assoprojetreponse

assoprojetpalettereponse = APIRouter()

class AssoProjetPaletteReponseCollectionResponse:
    def __init__(self, assos: List[m_AssoProjetPaletteReponse]):
        self.assos = assos

class AssoProjetPaletteReponseCollectionCreate(BaseModel):
    assos: List[AssoProjetPaletteReponseCreate]

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

@assoprojetpalettereponse.post("/assoprojetpalettereponse_collec/")
def rt_assoprojetpalettereponse_collec(collec: AssoProjetPaletteReponseCollectionCreate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        collec_d = dict(collec)
        print("collec : ", collec_d["assos"])
        for asso in collec_d["assos"]:
            projet_from_db = db.query(Projets).filter(Projets.id == asso.projet_id).first()
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
            
            palette_from_db = db.query(Palettes).filter(Palettes.id == asso.palette_id).first()
            if palette_from_db == None:
                raise HTTPException(status_code=404, detail="La palette n'existe pas")
            
            asso_owner_pal = db.query(AssoUserPalette).filter(AssoUserPalette.palette_id == palette_from_db.id).first()
            if asso_owner_pal == None:
                raise HTTPException(status_code=404, detail="La palette n'appartient a personne")
            
            if asso_owner_pal.user_id != user_id:
                raise HTTPException(status_code=404, detail="Vous n'avez pas acces à cette palette")
            
            reponse_from_db = db.query(Reponses).filter(Reponses.id == asso.reponse_id).first()
            if reponse_from_db == None:
                raise HTTPException(status_code=404, detail="La réponse n'existe pas")
            
            reponse_owner = db.query(AssoUserReponse).filter(AssoUserReponse.reponse_id == asso.reponse_id).first()
            if reponse_owner == None:
                raise HTTPException(status_code=404, detail="La reponse n'appartient à personne")

            if reponse_owner.user_id != user_id:
                raise HTTPException(status_code=404, detail="La reponse ne vous appartient pas")
            
            asso_projet_rep = db.query(AssoProjetReponse).filter((AssoProjetReponse.projet_id == asso.projet_id) & (AssoProjetReponse.reponse_id == asso.reponse_id)).first()
            if asso_projet_rep == None:
                assoprojetreponse_data = AssoProjetReponse(projet_id = asso.projet_id, reponse_id = asso.reponse_id)
                asso_projet_rep = create_assoprojetreponse(db, assoprojetreponse_data)
                
            
            asso_projet_pal_rep = db.query(m_AssoProjetPaletteReponse).filter((m_AssoProjetPaletteReponse.projet_id == asso.projet_id) & (m_AssoProjetPaletteReponse.reponse_id == asso.reponse_id) & (m_AssoProjetPaletteReponse.palette_id == asso.palette_id)).first()
            if asso_projet_pal_rep == None:
                assoprojetpalettereponse_data = dict(asso)
                print("create")
                a = create_assoprojetpalettereponse(db, assoprojetpalettereponse_data=assoprojetpalettereponse_data)
            else:
                print("received : ", asso, " \nasso_db : pro_id : ", asso_projet_pal_rep.projet_id, " pal_id: ", asso_projet_pal_rep.palette_id, " rep_id : ", asso_projet_pal_rep.reponse_id, " pos : ", asso_projet_pal_rep.position)
                
                if (asso.position != asso_projet_pal_rep.position):
                    print("update")
                    a = update_assoprojetpalettereponse(db, asso_projet_pal_rep.id, AssoProjetPaletteReponseUpdate(projet_id = asso.projet_id, palette_id=asso.palette_id, reponse_id=asso.reponse_id, position=asso.position))

        asso_projet_pal_rep_collec = db.query(m_AssoProjetPaletteReponse).filter(m_AssoProjetPaletteReponse.projet_id == projet_from_db.id).all()
        return AssoProjetPaletteReponseCollectionResponse(assos=asso_projet_pal_rep_collec)

        
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token invalide")