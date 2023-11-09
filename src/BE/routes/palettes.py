from config.db import get_db, Session
from pydantic import BaseModel
from typing import List
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE, TOKEN_EXPIRE, TOKEN_INVALIDE, TOKEN_NOT_SENT, USER_NOT_EXISTANT
from models.index import Palettes, Couleurs, AssoPaletteCouleur
from schemas.index import Palette, PaletteCreate, PaletteUpdate, CouleurCreate, AssoPaletteCouleurCreate, AssoUserPaletteCreate
from crud.palettes import create_palette, get_palette, update_palette, delete_palette  # Importez les fonctions spécifiques
from routes.couleurs import rt_find_couleur, rt_create_couleur
from crud.couleurs import create_couleur
from crud.assopalettecouleur import create_assopalettecouleur
from crud.assouserpalette import create_assouserpalette
from schemas.index import Couleur

palette = APIRouter()

class CouleurPosi(BaseModel):
    color: str
    position: int

class PaletteCreateFull(BaseModel):
    nom: str
    couleurs: List[CouleurPosi]


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
    return new_palette


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

@palette.delete("/palettes/{palette_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_palette(palette_id: int, db: Session = Depends(get_db)):
    success = delete_palette(db, palette_id)
    if not success:
        raise HTTPException(status_code=404, detail="Palette not found")
    return None

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
