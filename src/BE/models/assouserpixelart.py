from sqlalchemy import Column, Integer, ForeignKey
from app.config.database import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserPixelArt"
class AssoUserPixelArt(Base):
    __tablename__ = "AssoUserPixelArt"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    pixelart_id = Column(Integer, ForeignKey("pixelarts.id"), primary_key=True)
