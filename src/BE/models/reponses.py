from sqlalchemy import Column, Integer, String, Text
from config.db import Base

# Modèle SQLAlchemy pour la table "Reponses"
class Reponses(Base):
    __tablename__ = "Reponses"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(Text)
    fonction = Column(Text)  # Stockez ici les fonctions ou données de réponse
    ennonce = Column(Text)
    genre = Column(Text)
    # Autres colonnes de réponse, ajoutez-les ici si nécessaire
