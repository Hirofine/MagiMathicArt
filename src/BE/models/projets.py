from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from config.db import Base

# Modèle SQLAlchemy pour la table "Projets"
class Projets(Base):
    __tablename__ = "Projets"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(Text)

    # Autres colonnes de projet, ajoutez-les ici si nécessaire
