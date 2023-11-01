from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPixelArt"
class AssoProjetPixelArt(Base):
    __tablename__ = "AssoProjetPixelArt"

    id = Column(Integer, primary_key=True, index=True)
    projet_id = Column(Integer, ForeignKey("Projets.id"))
    pixelart_id = Column(Integer, ForeignKey("PixelArts.id"))
