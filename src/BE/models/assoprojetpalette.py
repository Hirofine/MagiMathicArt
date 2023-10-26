from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPalette"
class AssoProjetPalette(Base):
    __tablename__ = "AssoProjetPalette"

    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)
    palette_id = Column(Integer, ForeignKey("palettes.id"), primary_key=True)