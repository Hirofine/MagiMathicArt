from sqlalchemy import Column, Integer, String, Text, LargeBinary
from app.config.database import Base

# Modèle SQLAlchemy pour la table "Images"
class Image(Base):
    __tablename__ = "Images"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String, index=True)
    description = Column(Text)
    image = Column(LargeBinary)
    # Autres colonnes d'image, ajoutez-les ici si nécessaire
