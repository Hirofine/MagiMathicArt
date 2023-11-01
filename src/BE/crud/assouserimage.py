from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoUserImage  # Importez ici le modèle AssoUserImages

# Fonction spécifique pour créer un utilisateur
def create_assouserimage(db: Session, assouserimage_data):
    return crud.create(db, AssoUserImage, assouserimage_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assouserimage(db: Session, assouserimage_id):
    return crud.read(db, AssoUserImage, assouserimage_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assouserimage(db: Session, assouserimage_id, assouserimage_data):
    return crud.update(db, AssoUserImage, assouserimage_id, assouserimage_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assouserimage(db: Session, assouserimage_id):
    try:
        crud.delete(db, AssoUserImage, assouserimage_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
