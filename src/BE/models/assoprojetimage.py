from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetImage"
class AssoProjetImage(Base):
    __tablename__ = "AssoProjetImage"

    id = Column(Integer, primary_key=True, index=True)
    projet_id = Column(Integer, ForeignKey("Projets.id"))
    image_id = Column(Integer, ForeignKey("Images.id"))
    coordX = Column(Integer)
    coordY = Column(Integer)
    opacite = Column(Integer)
    dimX = Column(Integer)
    dimY = Column(Integer)