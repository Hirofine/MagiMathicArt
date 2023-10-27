from sqlalchemy import Column, Integer, String, Text
from config.db import Base

# Modèle SQLAlchemy pour la table "Palettes"
class Palettes(Base):
    __tablename__ = "Palettes"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    # D'autres colonnes pour les informations de la palette, ajoutez-les ici si nécessaire
