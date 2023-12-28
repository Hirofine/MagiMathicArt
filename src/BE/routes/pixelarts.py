from config.db import get_db, Session
from sqlalchemy import text, or_
from fastapi import APIRouter, Depends, HTTPException, File, UploadFile, status, Request
from fastapi.responses import StreamingResponse, FileResponse
from helper import verify_token, user_id_from_token, TOKEN_VALIDE
from models.index import PixelArts, AssoUserProjet, AssoProjetPixelArt, AssoUserPixelArt, AssoProjetPalette, Palettes, AssoPaletteCouleur, Couleurs
from schemas.index import PixelArt, PixelArtCreate, PixelArtUpdate, AssoUserPixelArtCreate
from crud.pixelarts import create_pixelart, get_pixelart, update_pixelart, delete_pixelart  # Importez les fonctions spécifiques
from crud.projets import get_projet
from crud.assouserpixelart import create_assouserpixelart
from PIL import Image, ImageDraw, ImageFont
import json
import matplotlib.pyplot as plt

pixelart = APIRouter()

@pixelart.post("/pixelarts/", response_model=PixelArt)
def rt_create_pixelart(pixelart: PixelArtCreate, request: Request, db: Session = Depends(get_db)):
    tok_val = verify_token(request, db)
    if(tok_val == TOKEN_VALIDE):
        user_id = user_id_from_token(request, db)
       
        pixelart_data = dict(pixelart)  # Convertit l'objet PixelArtCreate en dictionnaire
        pixel_art = create_pixelart(db, pixelart_data)

        data = dict(AssoUserPixelArtCreate(user_id = user_id, pixelart_id = pixel_art.id))
        assouserpixart = create_assouserpixelart(db, data)
        if assouserpixart == None:
            raise HTTPException(status_code=404, detail="Error when creating pixelart")

    return pixel_art

@pixelart.get("/pixelarts/{pixelart_id}", response_model=PixelArt)
def rt_read_pixelart(pixelart_id: int, db: Session = Depends(get_db)):
    pixelart = get_pixelart(db, pixelart_id)
    if pixelart is None:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return pixelart

@pixelart.get("/pixelart_from_projet/{projet_id}")
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
        
        assoprojetpixelart = db.query(AssoProjetPixelArt).filter(AssoProjetPixelArt.projet_id == projet_id).first()
        if assoprojetpixelart == None:
            raise HTTPException(status_code=404, detail="Pas de pixelart associée à ce projet")

        pixelart_id = assoprojetpixelart.pixelart_id
        pixelart = get_pixelart(db, pixelart_id)
        if pixelart is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(pixelart_id == AssoUserPixelArt.pixelart_id).first()

        if pixelart_owner == None:
            raise HTTPException(status_code=404, detail="Pas d'utilisateur associé à ce pixel_art")
        
        if pixelart_owner.user_id != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à ce pixelart")

        return pixelart
    else :
        raise HTTPException(status_code=404, detail="Palette not found")

@pixelart.put("/pixelarts/{pixelart_id}", response_model=PixelArt)
def rt_update_pixelart(pixelart_id: int, pixelart: PixelArtUpdate, db: Session = Depends(get_db)):
    updated_pixelart = update_pixelart(db, pixelart_id, pixelart)
    if updated_pixelart is None:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return updated_pixelart

@pixelart.put("/pixelarts_from_projet/{projet_id}", response_model=PixelArt)
def rt_update_pixelart(projet_id: int, pixelart: PixelArtUpdate, request: Request, db: Session = Depends(get_db)):
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
        
        assoprojetpixelart = db.query(AssoProjetPixelArt).filter(AssoProjetPixelArt.projet_id == projet_id).first()
        if assoprojetpixelart == None:
            raise HTTPException(status_code=404, detail="Pas de pixelart associée à ce projet")

        pixelart_id = assoprojetpixelart.pixelart_id
        pixelart_db = get_pixelart(db, pixelart_id)
        if pixelart_db is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(pixelart_id == AssoUserPixelArt.pixelart_id).first()

        if pixelart_owner == None:
            raise HTTPException(status_code=404, detail="Pas d'utilisateur associé à ce pixel_art")
        
        if pixelart_owner.user_id != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à ce pixelart")
        
        updated_pixelart = update_pixelart(db, pixelart_id, pixelart)
        if updated_pixelart is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        return updated_pixelart
    raise HTTPException(status_code=404, detail="Erreur lors de la verification de connexion")
        

@pixelart.delete("/pixelarts/{pixelart_id}", status_code=status.HTTP_204_NO_CONTENT)
def rt_delete_pixelart(pixelart_id: int, db: Session = Depends(get_db)):
    success = delete_pixelart(db, pixelart_id)
    if not success:
        raise HTTPException(status_code=404, detail="PixelArt not found")
    return None

@pixelart.get("/export_png/{projet_id}")
def rt_export_png_pixelart(projet_id: int, request: Request, db: Session = Depends(get_db)):
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
        
        assoprojetpixelart = db.query(AssoProjetPixelArt).filter(AssoProjetPixelArt.projet_id == projet_id).first()
        if assoprojetpixelart == None:
            raise HTTPException(status_code=404, detail="Pas de pixelart associée à ce projet")

        pixelart_id = assoprojetpixelart.pixelart_id
        pixelart_db = get_pixelart(db, pixelart_id)
        if pixelart_db is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(pixelart_id == AssoUserPixelArt.pixelart_id).first()

        if pixelart_owner == None:
            raise HTTPException(status_code=404, detail="Pas d'utilisateur associé à ce pixel_art")
        
        if pixelart_owner.user_id != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à ce pixelart")

        pixelArt = db.query(PixelArts).filter(pixelart_id == PixelArts.id).first()
        assoprojpal = db.query(AssoProjetPalette).filter(projet_id == AssoProjetPalette.projet_id).first()
        palette = db.query(Palettes).filter(assoprojpal.palette_id == Palettes.id).first()
        assopalcoul = db.query(AssoPaletteCouleur).filter(palette.id == AssoPaletteCouleur.palette_id).all()

        couleurs = []
        for asso in assopalcoul:
            couleurs.append([asso.position, db.query(Couleurs).filter(asso.couleur_id == Couleurs.id).first().color])
        couleurs.sort(key=lambda x: x[0])
        print(couleurs)
        data = json.loads(pixelArt.art)
        #print(data)
        pixels = []
        for y in range(pixelArt.dimensionsY):
            for x in range(pixelArt.dimensionsX):
                pixels.append(couleurs[int(data["pixels"][x + y * pixelArt.dimensionsX][2])][1])

        print(pixels)
        pixel_size = 50
        image = Image.new("RGB", (pixelArt.dimensionsX * pixel_size, pixelArt.dimensionsY * pixel_size))

        # Chargez les données de pixel dans l'image
        pixel_index = 0
        
        draw = ImageDraw.Draw(image)
        for x in range(pixelArt.dimensionsX):
            for y in range(pixelArt.dimensionsY):

                # Exemple : Vous pouvez définir les couleurs basées sur les valeurs de pixels ici
                # En supposant que les valeurs de pixel sont des couleurs en format RGB (ex: 0xFFFFFF pour blanc)
                color_value = pixels[pixel_index]  # Obtenez la valeur du pixel depuis les données
                couleur_rgb = tuple(int(color_value[i:i+2], 16) for i in (1, 3, 5))
                # Définissez la couleur du pixel dans l'image
                #image.putpixel((x, y), couleur_rgb)  # Exemple : Niveaux de gris
                draw.rectangle([x*pixel_size, y* pixel_size, (x+1)* pixel_size, (y+1) * pixel_size], fill=couleur_rgb)
                pixel_index += 1

        # Sauvegardez l'image en format PNG
        image.save("static/temp/pixel_art.png", "PNG")

        return FileResponse("static/temp/pixel_art.png", media_type="image/png", filename="pixel_art.png")


    raise HTTPException(status_code=404, detail="Erreur lors de la verification de la connexion")

@pixelart.get("/export_png_compile/{projet_id}")
def rt_export_png_compile_pixelart(projet_id: int, request: Request, db: Session = Depends(get_db)):
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
        
        assoprojetpixelart = db.query(AssoProjetPixelArt).filter(AssoProjetPixelArt.projet_id == projet_id).first()
        if assoprojetpixelart == None:
            raise HTTPException(status_code=404, detail="Pas de pixelart associée à ce projet")

        pixelart_id = assoprojetpixelart.pixelart_id
        pixelart_db = get_pixelart(db, pixelart_id)
        if pixelart_db is None:
            raise HTTPException(status_code=404, detail="PixelArt not found")
        
        pixelart_owner = db.query(AssoUserPixelArt).filter(pixelart_id == AssoUserPixelArt.pixelart_id).first()

        if pixelart_owner == None:
            raise HTTPException(status_code=404, detail="Pas d'utilisateur associé à ce pixel_art")
        
        if pixelart_owner.user_id != user_id:
            raise HTTPException(status_code=404, detail="Vous n'avez pas accés à ce pixelart")

        pixelArt = db.query(PixelArts).filter(pixelart_id == PixelArts.id).first()
        assoprojpal = db.query(AssoProjetPalette).filter(projet_id == AssoProjetPalette.projet_id).first()
        palette = db.query(Palettes).filter(assoprojpal.palette_id == Palettes.id).first()
        assopalcoul = db.query(AssoPaletteCouleur).filter(palette.id == AssoPaletteCouleur.palette_id).all()

        couleurs = []
        for asso in assopalcoul:
            couleurs.append([asso.position, db.query(Couleurs).filter(asso.couleur_id == Couleurs.id).first().color])
        couleurs.sort(key=lambda x: x[0])
        print(couleurs)
        data = json.loads(pixelArt.art)
        #print(data)
        pixels = []
        for y in range(pixelArt.dimensionsY):
            for x in range(pixelArt.dimensionsX):
                pixels.append(couleurs[int(data["pixels"][x + y * pixelArt.dimensionsX][2])][1])

        print(pixels)
        pixel_size = 100
        image = Image.new("RGB", (pixelArt.dimensionsX * pixel_size, pixelArt.dimensionsY * pixel_size))

        # Chargez les données de pixel dans l'image
        pixel_index = 0
        
        draw = ImageDraw.Draw(image)
        for x in range(pixelArt.dimensionsX):
            for y in range(pixelArt.dimensionsY):

                # Exemple : Vous pouvez définir les couleurs basées sur les valeurs de pixels ici
                # En supposant que les valeurs de pixel sont des couleurs en format RGB (ex: 0xFFFFFF pour blanc)
                color_value = pixels[pixel_index]  # Obtenez la valeur du pixel depuis les données
                couleur_rgb = tuple(int(color_value[i:i+2], 16) for i in (1, 3, 5))
                # Définissez la couleur du pixel dans l'image
                #image.putpixel((x, y), couleur_rgb)  # Exemple : Niveaux de gris
                draw.rectangle([x*pixel_size, y* pixel_size, (x+1)* pixel_size, (y+1) * pixel_size], fill=couleur_rgb)
                pixel_index += 1
        
        police = ImageFont.truetype("/usr/share/fonts/truetype/ubuntu/Ubuntu-M.ttf", 40)  # Utilisez un chemin absolu ou relatif vers la police souhaitée
        texte = "l|100"  # Texte à afficher

        # Position et couleur du texte
        position = (0, 0)  # Position du coin supérieur gauche du texte
        couleur_texte = (0, 0, 0)  # Couleur du texte en RGB

        # Dessiner le texte sur l'image
        draw.text(position, texte, fill=couleur_texte, font=police)
        position = (12, 52)
        draw.text(position, texte, fill=couleur_texte, font=police)
        # Sauvegardez l'image en format PNG
        image.save("static/temp/pixel_art.png", "PNG")

        nb_cases_x, nb_cases_y = 5, 5  # Nombre de cases en largeur et hauteur

        # Création d'une figure Matplotlib
        fig, ax = plt.subplots()
        ax.axis('on')
        ax.plot([-1, -1], [-1, nb_cases_y], color='black')
        ax.plot([-1, nb_cases_x], [-1, -1], color='black')
        # Dessiner la grille de cases et placer du texte LaTeX
        for i in range(nb_cases_x + 1):
            # Dessiner les lignes verticales
            ax.plot([i, i], [-1, nb_cases_y], color='black')
            for j in range(nb_cases_y + 1):
                # Dessiner les lignes horizontales
                ax.plot([-1, nb_cases_x], [j, j], color='black')

                # Coordonnées de chaque case
                x, y = i - 0.5, j - 0.5
                
                # Placer du texte LaTeX dans chaque case
                texte_latex = r'$\frac{1}{' + str(i) + ',' + str(j) + '}$'  # Exemple de texte LaTeX avec fractions

                ax.text(x, y, texte_latex, ha='center', va='center', fontsize=12)

        # Ajuster les limites pour afficher correctement la grille
        ax.set_xlim(-1.5, nb_cases_x + 0.5)
        ax.set_ylim(-1.5, nb_cases_y + 0.5)

        # Enregistrer l'image ou l'afficher
        plt.savefig('image_tex.png')

        return FileResponse("static/temp/pixel_art.png", media_type="image/png", filename="pixel_art.png")


    raise HTTPException(status_code=404, detail="Erreur lors de la verification de la connexion")

# Vous pouvez ajouter d'autres routes liées aux utilisateurs au besoin
