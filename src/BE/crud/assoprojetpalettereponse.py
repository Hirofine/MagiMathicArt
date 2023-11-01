from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoProjetPaletteReponse  # Importez ici le modèle AssoProjetPaletteReponses

# Fonction spécifique pour créer un utilisateur
def create_assoprojetpalettereponse(db: Session, assoprojetpalettereponse_data):
    return crud.create(db, AssoProjetPaletteReponse, assoprojetpalettereponse_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assoprojetpalettereponse(db: Session, assoprojetpalettereponse_id):
    return crud.read(db, AssoProjetPaletteReponse, assoprojetpalettereponse_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assoprojetpalettereponse(db: Session, assoprojetpalettereponse_id, assoprojetpalettereponse_data):
    return crud.update(db, AssoProjetPaletteReponse, assoprojetpalettereponse_id, assoprojetpalettereponse_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assoprojetpalettereponse(db: Session, assoprojetpalettereponse_id):
    try:
        crud.delete(db, AssoProjetPaletteReponse, assoprojetpalettereponse_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé