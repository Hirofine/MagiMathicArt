from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Palettes  # Importez ici le modèle Palettes

# Fonction spécifique pour créer un utilisateur
def create_palette(db: Session, palette_data):
    return crud.create(db, Palettes, palette_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_palette(db: Session, palette_id):
    return crud.read(db, Palettes, palette_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_palette(db: Session, palette_id, palette_data):
    return crud.update(db, Palettes, palette_id, palette_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_palette(db: Session, palette_id):
    try:
        crud.delete(db, Palettes, palette_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
