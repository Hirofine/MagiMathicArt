from sqlalchemy.orm import Session
from . import crud  # Importez ici le module crud générique
from models.index import AssoProjetReponse  # Importez ici le modèle AssoProjetReponses

# Fonction spécifique pour créer un utilisateur
def create_assoprojetreponse(db: Session, assoprojetreponse_data):
    return crud.create(db, AssoProjetReponse, assoprojetreponse_data)

# Fonction spécifique pour obtenir un utilisateur par ID
def get_assoprojetreponse(db: Session, assoprojetreponse_id):
    return crud.read(db, AssoProjetReponse, assoprojetreponse_id)

# Fonction spécifique pour mettre à jour un utilisateur par ID
def update_assoprojetreponse(db: Session, assoprojetreponse_id, assoprojetreponse_data):
    return crud.update(db, AssoProjetReponse, assoprojetreponse_id, assoprojetreponse_data)

# Fonction spécifique pour supprimer un utilisateur par ID
def delete_assoprojetreponse(db: Session, assoprojetreponse_id):
    try:
        crud.delete(db, AssoProjetReponse, assoprojetreponse_id)
        return True  # Indique que l'utilisateur a été supprimé
    except:
        return False  # Indique que l'utilisateur n'a pas été trouvé