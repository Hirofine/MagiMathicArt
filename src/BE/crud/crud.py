from sqlalchemy.orm import Session
from models.index import Users, Projets, Palettes, Couleurs, Images, PixelArts, Reponses
from models.index import AssoPaletteCouleur, AssoProjetImage, AssoProjetPalette, AssoProjetPaletteReponse
from models.index import AssoProjetPixelArt, AssoProjetReponse, AssoUserImage, AssoUserPalette
from models.index import AssoUserPixelArt, AssoUserProjet, AssoUserReponse  # Importez ici tous vos modèles

# Fonction générique pour créer un enregistrement
def create(db: Session, model, data):
    db_model = model(**data)
    db.add(db_model)
    db.commit()
    db.refresh(db_model)
    return db_model

# Fonction générique pour lire un enregistrement par ID
def read(db: Session, model, id):
    return db.query(model).filter(model.id == id).first()

# Fonction générique pour mettre à jour un enregistrement par ID
def update(db: Session, model, id, data):
    db.query(model).filter(model.id == id).update(data)
    db.commit()
    return read(db, model, id)

# Fonction générique pour supprimer un enregistrement par ID
def delete(db: Session, model, id):
    db.query(model).filter(model.id == id).delete()
    db.commit()

# Vous pouvez ajouter d'autres fonctions génériques au besoin

# Exemple d'utilisation : Fonction générique pour obtenir tous les enregistrements
def get_all(db: Session, model):
    return db.query(model).all()