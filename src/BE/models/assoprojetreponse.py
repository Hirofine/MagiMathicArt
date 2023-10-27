from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetReponse"
class AssoProjetReponse(Base):
    __tablename__ = "AssoProjetReponse"

    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)
    reponse_id = Column(Integer, ForeignKey("reponses.id"), primary_key=True)