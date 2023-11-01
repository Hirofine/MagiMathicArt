from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Images  # Importez ici le modèle Images

# Fonction spécifique pour créer un utilisateur
def create_image(db: Session, image_data):
    return crud.create(db, Images, image_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_image(db: Session, image_id):
    return crud.read(db, Images, image_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_image(db: Session, image_id, image_data):
    return crud.update(db, Images, image_id, image_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_image(db: Session, image_id):
    try:
        crud.delete(db, Images, image_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
