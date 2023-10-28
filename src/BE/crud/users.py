from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Users  # Importez ici le modèle Users

# Fonction spécifique pour créer un utilisateur
def create_user(db: Session, user_data):
    return crud.create(db, Users, user_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_user(db: Session, user_id):
    return crud.read(db, Users, user_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_user(db: Session, user_id, user_data):
    return crud.update(db, Users, user_id, user_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_user(db: Session, user_id):
    try:
        crud.delete(db, Users, user_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
