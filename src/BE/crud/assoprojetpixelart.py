from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoProjetPixelArt  # Importez ici le modèle AssoProjetPixelArts

# Fonction spécifique pour créer un utilisateur
def create_assoprojetpixelart(db: Session, assoprojetpixelart_data):
    return crud.create(db, AssoProjetPixelArt, assoprojetpixelart_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assoprojetpixelart(db: Session, assoprojetpixelart_id):
    return crud.read(db, AssoProjetPixelArt, assoprojetpixelart_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assoprojetpixelart(db: Session, assoprojetpixelart_id, assoprojetpixelart_data):
    return crud.update(db, AssoProjetPixelArt, assoprojetpixelart_id, assoprojetpixelart_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assoprojetpixelart(db: Session, assoprojetpixelart_id):
    try:
        crud.delete(db, AssoProjetPixelArt, assoprojetpixelart_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé