from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserPalette"
class AssoUserPalette(Base):
    __tablename__ = "AssoUserPalette"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    palette_id = Column(Integer, ForeignKey("Palettes.id"))