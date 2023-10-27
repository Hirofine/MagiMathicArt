from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPixelArt"
class AssoProjetPixelArt(Base):
    __tablename__ = "AssoProjetPixelArt"

    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)
    pixelart_id = Column(Integer, ForeignKey("pixelarts.id"), primary_key=True)
