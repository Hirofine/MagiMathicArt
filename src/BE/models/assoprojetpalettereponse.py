from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetPaletteReponse"
class AssoProjetPaletteReponse(Base):
    __tablename__ = "AssoProjetPaletteReponse"

    id = Column(Integer, primary_key=True, index=True)
    projet_id = Column(Integer, ForeignKey("Projets.id"))
    palette_id = Column(Integer, ForeignKey("Palettes.id"))
    reponse_id = Column(Integer, ForeignKey("Reponses.id"))
    position = Column(Integer)