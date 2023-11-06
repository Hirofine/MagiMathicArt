from sqlalchemy import Column, Integer, String, DateTime
from config.db import Base

# Modèle SQLAlchemy pour la table "Users"
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String, unique=True, index=True)
    passw = Column(String)
    token = Column(String, nullable=True)
    tokenExpi = Column(DateTime, nullable=True)
    tokenSalt = Column(String, nullable=True)
    # Autres colonnes d'utilisateur, ajoutez-les ici si nécessaire

