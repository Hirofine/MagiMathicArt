from sqlalchemy import Column, Integer, String
from app.config.database import Base

# Modèle SQLAlchemy pour la table "Users"
class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String, unique=True, index=True)
    pass = Column(String)
    # Autres colonnes d'utilisateur, ajoutez-les ici si nécessaire

