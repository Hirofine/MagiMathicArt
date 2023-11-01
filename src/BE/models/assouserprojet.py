from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserProjet"
class AssoUserProjet(Base):
    __tablename__ = "AssoUserProjet"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    projet_id = Column(Integer, ForeignKey("Projets.id"))