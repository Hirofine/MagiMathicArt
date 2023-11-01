from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoUserPalette  # Importez ici le modèle AssoUserPalettes

# Fonction spécifique pour créer un utilisateur
def create_assouserpalette(db: Session, assouserpalette_data):
    return crud.create(db, AssoUserPalette, assouserpalette_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assouserpalette(db: Session, assouserpalette_id):
    return crud.read(db, AssoUserPalette, assouserpalette_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assouserpalette(db: Session, assouserpalette_id, assouserpalette_data):
    return crud.update(db, AssoUserPalette, assouserpalette_id, assouserpalette_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assouserpalette(db: Session, assouserpalette_id):
    try:
        crud.delete(db, AssoUserPalette, assouserpalette_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
