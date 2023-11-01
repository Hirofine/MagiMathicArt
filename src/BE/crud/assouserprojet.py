from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoUserProjet  # Importez ici le modèle AssoUserProjets

# Fonction spécifique pour créer un utilisateur
def create_assouserprojet(db: Session, assouserprojet_data):
    return crud.create(db, AssoUserProjet, assouserprojet_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assouserprojet(db: Session, assouserprojet_id):
    return crud.read(db, AssoUserProjet, assouserprojet_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assouserprojet(db: Session, assouserprojet_id, assouserprojet_data):
    return crud.update(db, AssoUserProjet, assouserprojet_id, assouserprojet_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assouserprojet(db: Session, assouserprojet_id):
    try:
        crud.delete(db, AssoUserProjet, assouserprojet_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
