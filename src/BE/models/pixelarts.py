from sqlalchemy import Column, Integer, String, Text
from config.db import Base

# Modèle SQLAlchemy pour la table "PixelArts"
class PixelArts(Base):
    __tablename__ = "PixelArts"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(Text)
    dimensionsX = Column(Integer)
    dimensionsY = Column(Integer)
    art = Column(Text)  # Stockez ici les données de pixel art
    # Autres colonnes de pixel art, ajoutez-les ici si nécessaire
