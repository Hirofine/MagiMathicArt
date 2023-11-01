from sqlalchemy import Column, Integer, ForeignKey
from config.db import Base

# Modèle SQLAlchemy pour la table d'association "AssoUserPixelArt"
class AssoUserPixelArt(Base):
    __tablename__ = "AssoUserPixelArt"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    pixelart_id = Column(Integer, ForeignKey("PixelArts.id"))
