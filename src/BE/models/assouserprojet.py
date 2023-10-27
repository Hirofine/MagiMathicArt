from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserProjet"
class AssoUserProjet(Base):
    __tablename__ = "AssoUserProjet"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    projet_id = Column(Integer, ForeignKey("projets.id"), primary_key=True)