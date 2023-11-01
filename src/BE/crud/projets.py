from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Projets  # Importez ici le modèle Users

# Fonction spécifique pour créer un utilisateur
def create_projet(db: Session, projet_data):
    return crud.create(db, Projets, projet_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_projet(db: Session, projet_id):
    return crud.read(db, Projets, projet_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_projet(db: Session, projet_id, projet_data):
    return crud.update(db, Projets, projet_id, projet_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_projet(db: Session, projet_id):
    try:
        crud.delete(db, Projets, projet_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
