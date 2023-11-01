from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoProjetReponse"
class AssoProjetReponse(Base):
    __tablename__ = "AssoProjetReponse"

    id = Column(Integer, primary_key=True, index=True)
    projet_id = Column(Integer, ForeignKey("Projets.id"))
    reponse_id = Column(Integer, ForeignKey("Reponses.id"))