from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserReponse"
class AssoUserReponse(Base):
    __tablename__ = "AssoUserReponse"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    reponse_id = Column(Integer, ForeignKey("Reponses.id"))
