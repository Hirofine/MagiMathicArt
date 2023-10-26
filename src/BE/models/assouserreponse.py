from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserReponse"
class AssoUserReponse(Base):
    __tablename__ = "AssoUserReponse"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    reponse_id = Column(Integer, ForeignKey("reponses.id"), primary_key=True)
