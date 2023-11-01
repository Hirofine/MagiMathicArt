from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoProjetImage  # Importez ici le modèle AssoProjetImages

# Fonction spécifique pour créer un utilisateur
def create_assoprojetimage(db: Session, assoprojetimage_data):
    return crud.create(db, AssoProjetImage, assoprojetimage_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assoprojetimage(db: Session, assoprojetimage_id):
    return crud.read(db, AssoProjetImage, assoprojetimage_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assoprojetimage(db: Session, assoprojetimage_id, assoprojetimage_data):
    return crud.update(db, AssoProjetImage, assoprojetimage_id, assoprojetimage_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assoprojetimage(db: Session, assoprojetimage_id):
    try:
        crud.delete(db, AssoProjetImage, assoprojetimage_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
