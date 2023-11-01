from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import PixelArts  # Importez ici le modèle PixelArts

# Fonction spécifique pour créer un utilisateur
def create_pixelart(db: Session, pixelart_data):
    return crud.create(db, PixelArts, pixelart_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_pixelart(db: Session, pixelart_id):
    return crud.read(db, PixelArts, pixelart_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_pixelart(db: Session, pixelart_id, pixelart_data):
    return crud.update(db, PixelArts, pixelart_id, pixelart_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_pixelart(db: Session, pixelart_id):
    try:
        crud.delete(db, PixelArts, pixelart_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
