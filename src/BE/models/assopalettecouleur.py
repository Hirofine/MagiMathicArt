from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoPaletteCouleur"
class AssoPaletteCouleur(Base):
    __tablename__ = "AssoPaletteCouleur"
    
    id = Column(Integer, primary_key=True, index=True)
    palette_id = Column(Integer, ForeignKey("Palettes.id"))
    couleur_id = Column(Integer, ForeignKey("Couleurs.id"))
    position = Column(Integer)