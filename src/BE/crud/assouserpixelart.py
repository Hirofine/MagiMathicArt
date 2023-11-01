from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoUserPixelArt  # Importez ici le modèle AssoUserPixelArts

# Fonction spécifique pour créer un utilisateur
def create_assouserpixelart(db: Session, assouserpixelart_data):
    return crud.create(db, AssoUserPixelArt, assouserpixelart_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assouserpixelart(db: Session, assouserpixelart_id):
    return crud.read(db, AssoUserPixelArt, assouserpixelart_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assouserpixelart(db: Session, assouserpixelart_id, assouserpixelart_data):
    return crud.update(db, AssoUserPixelArt, assouserpixelart_id, assouserpixelart_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assouserpixelart(db: Session, assouserpixelart_id):
    try:
        crud.delete(db, AssoUserPixelArt, assouserpixelart_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
