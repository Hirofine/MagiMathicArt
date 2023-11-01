from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPalette"
class AssoProjetPalette(Base):
    __tablename__ = "AssoProjetPalette"

    id = Column(Integer, primary_key=True, index=True)
    projet_id = Column(Integer, ForeignKey("Projets.id"))
    palette_id = Column(Integer, ForeignKey("Palettes.id"))