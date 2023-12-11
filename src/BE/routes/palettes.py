from config.db import get_db, Session
from pydantic import BaseModel
from typing import List
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE, TOKEN_EXPIRE, TOKEN_INVALIDE, TOKEN_NOT_SENT, USER_NOT_EXISTANT
from models.index import Palettes, Couleurs, AssoPaletteCouleur, AssoUserPalette, AssoUserProjet, AssoProjetPalette
from schemas.index import Palette, PaletteCreate, PaletteUpdate, CouleurCreate, AssoPaletteCouleurCreate, AssoUserPaletteCreate
from crud.palettes import create_palette, get_palette, update_palette, delete_palette  # Importez les fonctions spécifiques
from crud.projets import get_projet
from crud.assouserprojet import get_assouserprojet
from crud.assoprojetpalette import get_assoprojetpalette
from routes.couleurs import rt_find_couleur, rt_create_couleur
from crud.couleurs import create_couleur
from crud.assopalettecouleur import create_assopalettecouleur, update_assopalettecouleur, delete_assopalettecouleur
from crud.assouserpalette import create_assouserpalette
from schemas.index import Couleur

palette = APIRouter()

class CouleurPosi(BaseModel):
    color: str
    position: int

class PaletteCreateFull(BaseModel):
    nom: str
    couleurs: List[CouleurPosi]

class PaletteReturnFull(BaseModel):
    nom: str
    couleurs: List[CouleurPosi]
    id: int


@palette.post("/palettes/", response_model=Palette)
def rt_create_palette(palette: PaletteCreateFull, request: Request, db: Session = Depends(get_db)):
    print(palette)
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        print("thingy")
        palette_data = dict(palette)  # Convertit l'objet PaletteCreate en dictionnaire
        print(palette_data)

        # Create Palette
        new_palette = create_palette(db, dict(PaletteCreate(nom = palette_data["nom"])))

        # Create Colors if necessary and Create AssoPaletteCouleurs
        color_ids = []
        for color_data in palette_data["couleurs"]:
            print(color_data)
            color_code = color_data.color
            existing_color = db.query(Couleurs).filter(Couleurs.color == color_code).first()
            print(existing_color)
            if existing_color:
                color_id = existing_color
            else:
                color_id = create_couleur(db, dict(CouleurCreate(color=color_code)))
            
            color_ids.append(color_id.id)
            create_assopalettecouleur(db, dict(AssoPaletteCouleurCreate(palette_id = new_palette.id, couleur_id = color_id.id, position = color_data.position)))
        
        # associate to user with AssoUserPalette
        user_id = user_id_from_token(request, db)
        create_assouserpalette(db, dict(user_id=user_id, palette_id = new_palette.id))
    else:
        print("c'est la mierda??  ", tok_val)
    
    print (new_palette)
    return new_palette

@palette.get("/palette_full/{palette_id}")
def rt_read_palette_full(palette_id: int, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        palette = get_palette(db, palette_id)
        if palette is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        palette_owner = db.query(AssoUserPalette).filter(palette_id == AssoUserPalette.palette_id).first().user_id
        if palette_owner != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")

        asso_couleurs = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id).order_by(AssoPaletteCouleur.position).all()
        couleurs : List[CouleurPosi] = []
        for asso in asso_couleurs:
            coul = db.query(Couleurs).filter(Couleurs.id == asso.couleur_id).first()
            couleurs.append(CouleurPosi(color = coul.color, position = asso.position))
        
        new_palette = PaletteReturnFull(nom = palette.nom, couleurs = couleurs, id=palette_id)
        return new_palette
    else :
        raise HTTPException(status_code=404, detail="Palette not found")
    
@palette.get("/palette_full_from_projet/{projet_id}")
def rt_read_palette_full(projet_id: int, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        projet = get_projet(db, projet_id)
        if projet == None:
            raise HTTPException(status_code=404, detail="Projet not found")
        
        assouserprojet = db.query(AssoUserProjet).filter(AssoUserProjet.projet_id == projet_id).first()
        if assouserprojet == None:
            raise HTTPException(status_code=404, detail="Projet not associated to a user")
        
        if assouserprojet.user_id != user_id:
            raise HTTPException(status_code=404, detail="User not allowed to access")
        
        assoprojetpalette = db.query(AssoProjetPalette).filter(AssoProjetPalette.projet_id == projet_id).first()
        if assoprojetpalette == None:
            raise HTTPException(status_code=404, detail="Pas de palette associée à ce projet")

        palette_id = assoprojetpalette.palette_id
        palette = get_palette(db, palette_id)
        if palette is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        palette_owner = db.query(AssoUserPalette).filter(palette_id == AssoUserPalette.palette_id).first().user_id
        if palette_owner != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")

        asso_couleurs = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id).order_by(AssoPaletteCouleur.position).all()
        couleurs : List[CouleurPosi] = []
        for asso in asso_couleurs:
            coul = db.query(Couleurs).filter(Couleurs.id == asso.couleur_id).first()
            couleurs.append(CouleurPosi(color = coul.color, position = asso.position))
        
        new_palette = PaletteReturnFull(nom = palette.nom, couleurs = couleurs, id=palette_id)
        return new_palette
    else :
        raise HTTPException(status_code=404, detail="Palette not found")

@palette.get("/palettes/{palette_id}", response_model=Palette)
def rt_read_palette(palette_id: int, db: Session = Depends(get_db)):
    palette = get_palette(db, palette_id)
    if palette is None:
        raise HTTPException(status_code=404, detail="Palette not found")
    return palette

@palette.put("/palettes/{palette_id}", response_model=Palette)
def rt_update_palette(palette_id: int, palette: PaletteUpdate, db: Session = Depends(get_db)):
    updated_palette = update_palette(db, palette_id, palette)
    if updated_palette is None:
        raise HTTPException(status_code=404, detail="Palette not found")
    return updated_palette


@palette.put("/palettes_full/{palette_id}", response_model=Palette)
def rt_create_palette(palette_id: int, palette: PaletteCreateFull, request: Request, db: Session = Depends(get_db)):
    print(palette)
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
        palette_orig = get_palette(db, palette_id)
        if palette is None:
            raise HTTPException(status_code=404, detail="Palette not found")
        
        palette_user = db.query(AssoUserPalette).filter(palette_id == AssoUserPalette.palette_id).first()
        palette_owner = palette_user.user_id
        if palette_owner != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")


        asso_couleurs = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id).order_by(AssoPaletteCouleur.position).all()
        couleurs : List[CouleurPosi] = []
        for asso in asso_couleurs:
            coul = db.query(Couleurs).filter(Couleurs.id == asso.couleur_id).first()
            couleurs.append(CouleurPosi(color = coul.color, position = asso.position))
        
        palette_orig_full = PaletteCreateFull(nom = palette_orig.nom, couleurs = couleurs)

        print("thingy")
        palette_data = dict(palette)  # Convertit l'objet PaletteCreate en dictionnaire
        print(palette_data)
        print("ancienne version")
        palette_orig_data = dict(palette_orig_full)
        print(palette_orig_data)

        
        #compare differences
        len_pd = len(palette_data["couleurs"])
        len_pod = len(palette_orig_data["couleurs"])

        if  len_pd > len_pod:
            print("couleurs ajoutées")
            for color, color_orig in zip(palette_data["couleurs"], palette_orig_data["couleurs"]):
                if color.color != color_orig.color:
                    print("couleur changée")
                    couleur = db.query(Couleurs).filter(color.color == Couleurs.color).first()
                    if couleur != None:
                        couleur_id = couleur.id
                    else:
                        couleur_id = create_couleur(db, dict(CouleurCreate(color=color.color))).id

                    asso = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id, color.position == AssoPaletteCouleur.position).first()
                    asso = update_assopalettecouleur(db, asso.id, AssoPaletteCouleurCreate(palette_id = asso.palette_id, position = asso.position, couleur_id = couleur_id))
                else:
                    print("pas de changements")

            for color in palette_data["couleurs"]:
                if (color.position >= len_pod):
                    couleur = db.query(Couleurs).filter(color.color == Couleurs.color).first()
                    if couleur != None:
                        couleur_id = couleur.id
                    else:
                        couleur_id = create_couleur(db, dict(CouleurCreate(color=color.color))).id
                    asso = create_assopalettecouleur(db, dict(AssoPaletteCouleurCreate(palette_id = palette_id, couleur_id = couleur_id, position = color.position)))

        elif len_pd < len_pod:
            print("couleurs supprimés")
            for color, color_orig in zip(palette_data["couleurs"], palette_orig_data["couleurs"]):
                if color.color != color_orig.color:
                    print("couleur changée")
                    couleur = db.query(Couleurs).filter(color.color == Couleurs.color).first()
                    if couleur != None:
                        couleur_id = couleur.id
                    else:
                        couleur_id = create_couleur(db, dict(CouleurCreate(color=color.color))).id

                    asso = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id, color.position == AssoPaletteCouleur.position).first()
                    asso = update_assopalettecouleur(db, asso.id, AssoPaletteCouleurCreate(palette_id = asso.palette_id, position = asso.position, couleur_id = couleur_id))
                else:
                    print("pas de changements")
            
            assos = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id, AssoPaletteCouleur.position >= len_pd ).all()
            for ass in assos:
                ass = delete_assopalettecouleur(db, ass.id)
        else:
            print("même nombre de couleurs")
            for color, color_orig in zip(palette_data["couleurs"], palette_orig_data["couleurs"]):
                if color.color != color_orig.color:
                    print("couleur changée")
                    couleur = db.query(Couleurs).filter(color.color == Couleurs.color).first()
                    if couleur != None:
                        couleur_id = couleur.id
                    else:
                        couleur_id = create_couleur(db, dict(CouleurCreate(color=color.color))).id

                    asso = db.query(AssoPaletteCouleur).filter(palette_id == AssoPaletteCouleur.palette_id, color.position == AssoPaletteCouleur.position).first()
                    asso = update_assopalettecouleur(db, asso.id, AssoPaletteCouleurCreate(palette_id = asso.palette_id, position = asso.position, couleur_id = couleur_id))
                else:
                    print("pas de changements")



        if palette_data["nom"] != palette_orig_data["nom"]:
            new_name = palette_data["nom"]
            palette = update_palette(db, palette_id, PaletteUpdate(nom=new_name))
            return palette
        return palette_orig
    else:
        print("c'est la mierda??  ", tok_val)
        raise HTTPException(status_code=404, detail="Vous n'avez pas accés à cette palette")

@palette.delete("/palettes/{palette_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_palette(palette_id: int, db: Session = Depends(get_db)):
    success = delete_palette(db, palette_id)
    if not success:
        raise HTTPException(status_code=404, detail="Palette not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
