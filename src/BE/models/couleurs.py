from sqlalchemy import Column, Integer, String
from config.db import Base

# Modèle SQLAlchemy pour la table "Couleurs"
class Couleurs(Base):
    __tablename__ = "Couleurs"

    id = Column(Integer, primary_key=True, index=True)
    color = Column(String, unique=True, index=True)
    # Autres colonnes de couleur, ajoutez-les ici si nécessaire

