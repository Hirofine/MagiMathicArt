from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserPalette"
class AssoUserPalette(Base):
    __tablename__ = "AssoUserPalette"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    palette_id = Column(Integer, ForeignKey("palettes.id"), primary_key=True)