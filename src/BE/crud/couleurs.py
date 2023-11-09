from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import Couleurs  # Importez ici le modèle Couleurs

# Fonction spécifique pour créer un utilisateur
def create_couleur(db: Session, couleur_data):
    return crud.create(db, Couleurs, couleur_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_couleur(db: Session, couleur_id):
    return crud.read(db, Couleurs, couleur_id)

def get_couleur_from_code(db: Session, color_code):
    return db.query(Couleurs).filter(Couleurs.color == color_code).first()

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_couleur(db: Session, couleur_id, couleur_data):
    return crud.update(db, Couleurs, couleur_id, couleur_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_couleur(db: Session, couleur_id):
    try:
        crud.delete(db, Couleurs, couleur_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
