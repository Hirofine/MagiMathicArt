from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetImage"
class AssoProjetImage(Base):
    __tablename__ = "AssoProjetImage"

    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)
    image_id = Column(Integer, ForeignKey("images.id"), primary_key=True)
    coordX = Column(Integer)
    coordY = Column(Integer)
    opacite = Column(Integer)
    dimX = Column(Integer)
    dimY = Column(Integer)