from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoPaletteCouleur  # Importez ici le modèle AssoPaletteCouleurs

# Fonction spécifique pour créer un utilisateur
def create_assopalettecouleur(db: Session, assopalettecouleur_data):
    return crud.create(db, AssoPaletteCouleur, assopalettecouleur_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assopalettecouleur(db: Session, assopalettecouleur_id):
    return crud.read(db, AssoPaletteCouleur, assopalettecouleur_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assopalettecouleur(db: Session, assopalettecouleur_id, assopalettecouleur_data):
    return crud.update(db, AssoPaletteCouleur, assopalettecouleur_id, assopalettecouleur_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assopalettecouleur(db: Session, assopalettecouleur_id):
    try:
        crud.delete(db, AssoPaletteCouleur, assopalettecouleur_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé
