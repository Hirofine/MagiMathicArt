from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoPaletteCouleur"
class AssoPaletteCouleur(Base):
    __tablename__ = "AssoPaletteCouleur"

    palette_id = Column(Integer, ForeignKey("palettes.id"), primary_key=True)
    couleur_id = Column(Integer, ForeignKey("couleurs.id"), primary_key=True)
    position = Column(Integer)