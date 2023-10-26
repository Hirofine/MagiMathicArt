from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPaletteReponse"
class AssoProjetPaletteReponse(Base):
    __tablename__ = "AssoProjetPaletteReponse"

    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)
    palette_id = Column(Integer, ForeignKey("palettes.id"), primary_key=True)
    reponse_id = Column(Integer, ForeignKey("reponses.id"), primary_key=True)
    position = Column(Integer)