from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Reponses  # Importez ici le modèle Reponses

# Fonction spécifique pour créer un utilisateur
def create_reponse(db: Session, reponse_data):
    return crud.create(db, Reponses, reponse_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_reponse(db: Session, reponse_id):
    return crud.read(db, Reponses, reponse_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_reponse(db: Session, reponse_id, reponse_data):
    return crud.update(db, Reponses, reponse_id, reponse_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_reponse(db: Session, reponse_id):
    try:
        crud.delete(db, Reponses, reponse_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé