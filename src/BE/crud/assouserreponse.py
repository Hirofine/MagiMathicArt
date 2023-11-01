from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoUserReponse  # Importez ici le modèle AssoUserReponses

# Fonction spécifique pour créer un utilisateur
def create_assouserreponse(db: Session, assouserreponse_data):
    return crud.create(db, AssoUserReponse, assouserreponse_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assouserreponse(db: Session, assouserreponse_id):
    return crud.read(db, AssoUserReponse, assouserreponse_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assouserreponse(db: Session, assouserreponse_id, assouserreponse_data):
    return crud.update(db, AssoUserReponse, assouserreponse_id, assouserreponse_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assouserreponse(db: Session, assouserreponse_id):
    try:
        crud.delete(db, AssoUserReponse, assouserreponse_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
