from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoProjetPalette  # Importez ici le modèle AssoProjetPalettes

# Fonction spécifique pour créer un utilisateur
def create_assoprojetpalette(db: Session, assoprojetpalette_data):
    return crud.create(db, AssoProjetPalette, assoprojetpalette_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assoprojetpalette(db: Session, assoprojetpalette_id):
    return crud.read(db, AssoProjetPalette, assoprojetpalette_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assoprojetpalette(db: Session, assoprojetpalette_id, assoprojetpalette_data):
    return crud.update(db, AssoProjetPalette, assoprojetpalette_id, assoprojetpalette_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assoprojetpalette(db: Session, assoprojetpalette_id):
    try:
        crud.delete(db, AssoProjetPalette, assoprojetpalette_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé